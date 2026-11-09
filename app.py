"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from datetime import datetime, timedelta, timezone
import os
import re
import uuid
from dotenv import load_dotenv
from flask import Flask, abort, flash, jsonify, redirect, render_template, request, url_for, send_from_directory
from flask_migrate import Migrate
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

from models import Service, Ticket, User, db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
SAVED_PDF = re.compile(r"^[0-9a-f]{32}\.pdf$")

os.makedirs(UPLOAD_DIR, exist_ok=True)

load_dotenv()

app = Flask(__name__)
app.secret_key = "dev-only-change-me"  # Week 11 moves this into an environment variable
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # Max of 16 MB per upload
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO") == "1"

db.init_app(app)
migrate = Migrate(app, db)

# Choices for the request form. The server checks every value against these lists.
COLOR_MODES = ["Grayscale", "Colored"]
PAPER_TYPES = ["Bond Paper", "Photo Paper", "Sticker Paper", "Cardstock"]
PAPER_SIZES = ["Short", "A4", "Long"]

# Status words, badge styles and tracker steps for the My Place page.
STATUS_LABELS = {
    "waiting": "Waiting",
    "printing": "Printing",
    "ready": "Ready for pickup",
    "done": "Done",
    "cancelled": "Cancelled",
}
STATUS_COLOR = {
    "waiting": "text-warning-emphasis",
    "printing": "text-primary-emphasis",
    "ready": "text-success-emphasis",
    "done": "text-dark-emphasis",
    "cancelled": "text-danger-emphasis",
}
STATUS_BADGE = {
    "waiting": "text-bg-warning",
    "printing": "text-bg-primary",
    "ready": "text-bg-success",
    "done": "text-bg-dark",
    "cancelled": "text-bg-danger",
}
# Filter choices for the staff table: (value in the URL, label on the button).
FILTERS = [
    ("waiting", "Waiting"),
    ("ready", "Ready"),
    ("done", "Done"),
    ("cancelled", "Cancelled"),
    ("all", "All requests"),
]
CHIP_STYLE = {
    "waiting": "chip-waiting",
    "ready": "chip-ready",
    "done": "chip-done",
    "cancelled": "chip-cancelled",
    "all": "chip-all",
}

PH_TIME = timezone(timedelta(hours=8))  # Philippine time has no daylight saving

@app.template_filter("local")
def local_time(value):
    """Show a database time in Philippine time, e.g. Nov 16, 08:01 AM."""
    return value.astimezone(PH_TIME).strftime("%b %d, %I:%M %p") if value else ""

def people_ahead(t):
    """Count tickets still waiting for the same service that joined before t."""
    stmt = (db.select(func.count())
            .select_from(Ticket)
            .where(Ticket.service_id == t.service_id,
                   Ticket.status == "waiting",
                   Ticket.created_at < t.created_at))
    return db.session.scalar(stmt)

def describe_ticket(ticket):
    status = ticket.status
    ahead = people_ahead(ticket) if status == "waiting" else 0
    match status:
        case "waiting":
            message = "You're next!" if ahead == 0 else (
                "1 request ahead of you" if ahead == 1 else f"{ahead} requests ahead of you")
        case "printing":
            message = "Your request is being printed."
        case "ready":
            message = "Ready! Please pick it up at the printing station."
        case "done":
            message = "Completed. Thank you!"
        case _:
            message = "This request was cancelled."
    return {
        "status": status,
        "label": STATUS_LABELS[status],
        "badge": STATUS_BADGE[status],
        "color": STATUS_COLOR[status],
        "ahead": ahead,
        "message": message
    }

def all_services():
    return db.session.scalars(db.select(Service).order_by(Service.name)).all()

def active_services():
    stmt = db.select(Service).filter_by(active=True).order_by(Service.name)
    return db.session.scalars(stmt).all()

def delete_pdf(t):
    """Delete the ticket's PDF from the server and forget its name (FR-12)."""
    if t.stored_name:
        path = os.path.join(UPLOAD_DIR, t.stored_name)
        if os.path.exists(path):
            os.remove(path)
        t.stored_name = None

def clean_name(text):
    """Remove extra spaces and capitalize each part: '  maria   dela CRUZ ' -> 'Maria Dela Cruz'."""
    return " ".join(text.split()).title()

def clock():
    return datetime.now().strftime("%I:%M %p").lstrip("0")

def form_context(form, errors, pending = None):
    return dict(form=form, 
                errors=errors,
                services=active_services(),
                pending=pending,
                color_modes=COLOR_MODES,
                paper_types=PAPER_TYPES, 
                paper_sizes=PAPER_SIZES)

@app.route("/")
def index():
    # render_template looks inside the templates/ folder and passes
    # keyword arguments to the template as variables.
    return render_template("index.html")

@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    return render_template("ticket.html",
                           ticket=t,
                           service=t.service,
                           info=describe_ticket(t),
                           first_name=t.user.first_name,
                           updated=clock())

@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    return jsonify({**describe_ticket(t), "updated": clock()})

@app.post("/queue/<int:ticket_id>/leave")
def leave(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    if t.status != "waiting":
        flash("Only a request that is still waiting can be cancelled.", "warning")
        return redirect(url_for("ticket", ticket_id=ticket_id))
    t.status = "cancelled"  # soft delete: the row stays for reports
    t.finished_at = func.now()
    delete_pdf(t)
    db.session.commit()
    flash(f"Request #{ticket_id} was cancelled. You can send a new request anytime.", "info")
    return redirect(url_for("index"))

def saved_pdf(name):
    """The stored name of a PDF kept from an earlier try, if it is safe and still on disk."""
    if SAVED_PDF.match(name or "") and os.path.exists(os.path.join(UPLOAD_DIR, name)):
        return name
    return None

@app.get("/pending-upload/<name>")
def pending_upload(name):
    """Return a previously saved PDF so the browser can display it in the file input."""
    stored_name = saved_pdf(name)

    if stored_name is None:
        abort(404)

    response = send_from_directory(
        UPLOAD_DIR,
        stored_name,
        mimetype="application/pdf",
        as_attachment=False
    )

    response.headers["Cache-Control"] = "no-store"
    return response

@app.get("/join")
def join_form():
    return render_template("join.html", **form_context({}, {}))

@app.post("/join")
def join():
    form = request.form
    first_name = clean_name(form.get("first_name", ""))
    last_name = clean_name(form.get("last_name", ""))
    service_id = form.get("service_id", type=int)
    service = db.session.get(Service, service_id) if service_id else None
    color_mode = form.get("color_mode", "")
    copies = form.get("number_of_copies", type=int)
    paper_type = form.get("paper_type", "")
    paper_size = form.get("paper_size", "")
    notes = form.get("notes", "").strip()
    upload = request.files.get("file")
    kept_name = saved_pdf(form.get("pending_file", ""))
    stored_name = kept_name 
    file_label = form.get("pending_label", "")[:120] if kept_name else ""

    errors = {}
    if not first_name:
        errors["first_name"] = "Enter your first name."
    elif len(first_name) > 60:
        errors["first_name"] = "Keep your first name under 60 characters."
    if not last_name:
        errors["last_name"] = "Enter your last name."
    elif len(last_name) > 60:
        errors["last_name"] = "Keep your last name under 60 characters."
    if not active_services():
        errors["service_id"] = "No service is active right now. Please try again later."
    elif service is None:
        errors["service_id"] = "Choose a service."
    elif not service.active:
        errors["service_id"] = "That service is not available anymore. Choose another one."

    # Check whether the user selected a NEW file.
    # An empty filename means no new file was selected.
    has_new_upload = upload is not None and bool(upload.filename)

    if has_new_upload:
        if not upload.filename.lower().endswith(".pdf"):
            errors["file"] = "Only PDF files are accepted. Save or export your file as a PDF first."

        elif upload.stream.read(5) != b"%PDF-":
            errors["file"] = "That file does not look like a valid PDF. Try exporting it again."

        else:
            # Save the valid PDF immediately, even if another field has an error.
            upload.stream.seek(0)

            new_stored_name = f"{uuid.uuid4().hex}.pdf"
            upload.save(os.path.join(UPLOAD_DIR, new_stored_name))

            # Replace the previous pending PDF, if one exists.
            if kept_name:
                old_path = os.path.join(UPLOAD_DIR, kept_name)
                if os.path.exists(old_path):
                    os.remove(old_path)

            stored_name = new_stored_name
            file_label = secure_filename(upload.filename) or "document.pdf"

    elif not kept_name:
        # No new file was selected and no previously uploaded PDF exists.
        errors["file"] = "Attach the PDF you want to be printed."

    if color_mode not in COLOR_MODES:
        errors["color_mode"] = "Choose Grayscale or Colored."
    if copies is None or not 1 <= copies <= 100:
        errors["number_of_copies"] = "Enter a number of copies from 1 to 100."
    if paper_type not in PAPER_TYPES:
        errors["paper_type"] = "Choose a paper type."
    if paper_size not in PAPER_SIZES:
        errors["paper_size"] = "Choose a paper size."
    if len(notes) > 300:
        errors["notes"] = "Keep additional instructions under 300 characters."

    pending = {"file": stored_name, "label": file_label} if stored_name else None

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", **form_context(form, errors, pending)), 400

    # Same first and last name (any capitalization) is the same person.
    user = db.session.scalar(
        db.select(User).filter_by(first_name=first_name, last_name=last_name)
    )
    if user is None:
        user = User(first_name=first_name, last_name=last_name)
    ticket = Ticket(
        user=user,
        service=service,
        file_name=file_label,
        stored_name=stored_name,
        color_mode=color_mode,
        copies=copies,
        paper_type=paper_type,
        paper_size=paper_size,
        notes=notes or None,
    )
    db.session.add(ticket)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Something went wrong saving your request. Please try again.", "danger")
        return render_template("join.html", **form_context(form, {}, pending)), 409

    flash(f"Request submitted. Your ticket is #{ticket.id}.", "success")
    return redirect(url_for("ticket", ticket_id=ticket.id))

def get_status_count_table(service_id=None):
    c = {key: 0 for key in STATUS_LABELS}
    stmt = db.select(Ticket.status, func.count()).group_by(Ticket.status)
    if service_id:
        stmt = stmt.where(Ticket.service_id == service_id)
    for status, number in db.session.execute(stmt):
        c[status] = number
    c["total"] = sum(c.values())
    return c


def waiting_list():
    """Waiting requests in the order they joined (oldest first)."""
    stmt = (db.select(Ticket)
            .where(Ticket.status == "waiting")
            .order_by(Ticket.created_at, Ticket.id))
    return db.session.scalars(stmt).all()


def current_printing():
    """The one request being printed right now, or None."""
    return db.session.scalar(db.select(Ticket).where(Ticket.status == "printing"))


@app.context_processor
def inject_status_words():
    return {"STATUS_LABELS": STATUS_LABELS, 
            "STATUS_BADGE": STATUS_BADGE,
            "STATUS_COLOR": STATUS_COLOR}

def chosen_filter(value):
    """Only known filter names are accepted; anything else falls back to Waiting."""
    return value if value in dict(FILTERS) else "waiting"

@app.get("/staff")
def staff_dashboard():
    view = chosen_filter(request.args.get("status"))
    service_id = request.args.get("service_id", type=int)
    stmt = db.select(Ticket).order_by(Ticket.created_at, Ticket.id)
    if view != "all":
        stmt = stmt.where(Ticket.status == view)
    if service_id:
        stmt = stmt.where(Ticket.service_id == service_id)
    rows = db.session.scalars(stmt).all()
    waiting = waiting_list()
    return render_template(
        "staff.html",
        printing=current_printing(),
        rows=rows,
        chip_style=CHIP_STYLE,
        filters=FILTERS,
        view=view,
        view_label=dict(FILTERS)[view],
        head_number=waiting[0].id if waiting else None,
        c=get_status_count_table(service_id),
        services=all_services(),
        selected=service_id,
    )

def back_to_dashboard():
    """Return to the dashboard with the same filter the staff member was looking at."""
    return redirect(url_for("staff_dashboard", status=chosen_filter(request.form.get("view"))))

def start_printing(ticket_id=None):
    """Move the oldest waiting request to printing."""
    waiting = waiting_list()
    busy = current_printing()
    if busy:
        flash(f"Ticket #{busy.id} is still printing. Mark it as ready first.", "warning")
    elif not waiting:
        flash("No one is waiting.", "info")
    elif ticket_id is not None and waiting[0].id != ticket_id:
        flash(f"First come, first served: ticket #{waiting[0].id} goes first.", "warning")
    else:
        t = waiting[0]
        t.status = "printing"
        t.printing_at = func.now()  # the database fills in the time
        try:
            db.session.commit()
            flash(f"Ticket #{t.id} is now printing.", "info")
        except IntegrityError:
            # Two staff clicked at once: the database allows only one printing ticket.
            db.session.rollback()
            flash("Another request is already printing.", "warning")

@app.post("/staff/call-next")
def staff_call_next():
    start_printing()
    return back_to_dashboard()

@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    if action not in ("start", "ready", "done", "cancel"):
        abort(404)
    t = db.get_or_404(Ticket, ticket_id)
    status = t.status

    if action == "start":
        if status != "waiting":
            flash(f"Ticket #{ticket_id} is not waiting.", "warning")
        else:
            start_printing(ticket_id)
    elif action == "ready":
        if status != "printing":
            flash("Only the request that is printing can be marked ready.", "warning")
        else:
            t.status = "ready"
            t.ready_at = func.now()
            db.session.commit()
            flash(f"Ticket #{ticket_id} is ready for pickup.", "success")
    elif action == "done":
        if status != "ready":
            flash("Only a ready request can be marked done.", "warning")
        else:
            t.status = "done"
            t.finished_at = func.now()
            delete_pdf(t)
            db.session.commit()
            flash(f"Ticket #{ticket_id} is done.", "success")
    else:  # cancel
        if status != "waiting":
            flash("Only a waiting request can be cancelled.", "warning")
        else:
            t.status = "cancelled"
            t.finished_at = func.now()
            delete_pdf(t)
            db.session.commit()
            flash(f"Ticket #{ticket_id} was cancelled.", "info")
    return back_to_dashboard()

@app.post("/staff/tickets/<int:ticket_id>/delete")
def delete_ticket(ticket_id):
    """Hard delete: the PDF goes first, then the ticket row. The user row stays."""
    t = db.get_or_404(Ticket, ticket_id)
    delete_pdf(t)
    db.session.delete(t)
    db.session.commit()
    flash(f"Ticket #{ticket_id} was deleted.", "warning")
    return back_to_dashboard()

@app.get("/staff/tickets/<int:ticket_id>/file")
def staff_file(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    if not saved_pdf(t.stored_name):
        abort(404)
    return send_from_directory(UPLOAD_DIR,
                               t.stored_name,
                               as_attachment=True,
                               download_name=t.file_name)

def clean_service_name(text):
    return " ".join(text.split())

@app.get("/staff/services/services.json")
def services_json():
    return jsonify([{"id": s.id, "name": s.name} for s in active_services()])

@app.get("/staff/services")
def services_list():
    return render_template("services.html", services=all_services())

@app.post("/staff/services")
def service_create():
    name = clean_service_name(request.form.get("name", ""))
    if not name or len(name) > 100:
        flash("Enter a service name (up to 100 characters).", "danger")
        return redirect(url_for("services_list"))
    db.session.add(Service(name=name))
    try:
        db.session.commit()
        flash(f"Service \"{name}\" added.", "success")
    except IntegrityError:
        db.session.rollback()
        flash(f"A service named \"{name}\" already exists.", "danger")
    return redirect(url_for("services_list"))

@app.post("/staff/services/<int:service_id>/edit")
def service_edit(service_id):
    s = db.get_or_404(Service, service_id)
    name = clean_service_name(request.form.get("name", ""))
    if not name or len(name) > 100:
        flash("Enter a service name (up to 100 characters).", "danger")
        return redirect(url_for("services_list"))
    s.name = name
    s.active = request.form.get("active") == "on"  # an unticked box is not sent at all
    try:
        db.session.commit()
        flash(f"Service \"{name}\" updated.", "success")
    except IntegrityError:
        db.session.rollback()
        flash(f"A service named \"{name}\" already exists.", "danger")
    return redirect(url_for("services_list"))

@app.post("/staff/services/<int:service_id>/delete")
def service_delete(service_id):
    s = db.get_or_404(Service, service_id)
    name = s.name
    if s.tickets:
        flash(f"\"{name}\" has tickets, so it cannot be deleted. Turn it off instead.", "danger")
        return redirect(url_for("services_list"))
    db.session.delete(s)
    db.session.commit()
    flash(f"Service \"{name}\" deleted.", "warning")
    return redirect(url_for("services_list"))

@app.errorhandler(RequestEntityTooLarge)
def too_large(_err):
    flash("That file is too large. The limit is 16 MB.", "danger")
    return render_template("join.html", **form_context({}, {"file": "Choose a PDF under 16 MB."})), 413

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.cli.command("seed")
def seed():
    """Add the starting services if they are not there yet."""
    starting = [("Printing")]
    for name in starting:
        exists = db.session.scalar(db.select(Service).filter_by(name=name))
        if exists is None:
            db.session.add(Service(name=name))
    db.session.commit()
    print("Services are ready.")

if __name__ == "__main__":
    app.run(debug=True)