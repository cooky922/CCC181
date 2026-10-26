"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from datetime import datetime
import os
import uuid
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)
app.secret_key = "dev-only-change-me"  # Week 11 moves this into an environment variable
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # Max of 16 MB per upload

SERVICES = [
    {"id": 1, "name": "Document Printing"},
]

# Choices for the request form. The server checks every value against these lists.
COLOR_MODES = ["Grayscale", "Colored"]
PAPER_TYPES = ["Bond Paper", "Photo Paper", "Sticker Paper", "Cardstock"]
PAPER_SIZES = ["Short", "A4", "Long"]

# Sample data for the demo. It lives in memory, so it resets every time the
# server restarts. A real app would save tickets in a database later.
TICKETS = [
    {
        "number": 1,
        "name": "Desmond Gold",
        "service_id": 1,
        "file_name": "assignment.pdf",
        "file_path": "uploads/assignment.pdf",
        "number_of_copies": 3,
        "paper_size": "A4",
        "paper_type": "Bond Paper",
        "color_mode": "Grayscale",
        "notes": "",
        "status": "waiting",
    },
    {
        "number": 2,
        "name": "Lex Ian",
        "service_id": 1,
        "file_name": "report.pdf",
        "file_path": "uploads/report.pdf",
        "number_of_copies": 1,
        "paper_size": "Long",
        "paper_type": "Bond Paper",
        "color_mode": "Colored",
        "notes": "",
        "status": "printing",
    },
]

# Status words, badge styles and tracker steps for the My Place page.
STATUS_LABELS = {
    "waiting": "Waiting",
    "printing": "Printing",
    "ready": "Ready for pickup",
    "done": "Done",
    "cancelled": "Cancelled",
}
STATUS_BADGE = {
    "waiting": "text-bg-warning",
    "printing": "text-bg-primary",
    "ready": "text-bg-success",
    "done": "text-bg-secondary",
    "cancelled": "text-bg-danger",
}
STEPS = ["waiting", "printing", "ready", "done"]
STEP_LABELS = ["Waiting", "Printing", "Ready", "Done"]

def get_ticket(number):
    return next((t for t in TICKETS if t["number"] == number), None)

def requests_ahead(t):
    return sum(1 for x in TICKETS
               if x["service_id"] == t["service_id"]
               and x["status"] == "waiting"
               and x["number"] < t["number"])

def describe(t):
    status = t["status"]
    ahead = requests_ahead(t) if status == "waiting" else 0
    if status == "waiting":
        message = "You're next!" if ahead == 0 else (
            "1 request ahead of you" if ahead == 1 else f"{ahead} requests ahead of you")
    elif status == "printing":
        message = "Your request is being printed."
    elif status == "ready":
        message = "Ready! Please pick it up at the printing station."
    elif status == "done":
        message = "Completed. Thank you!"
    else:
        message = "This request was cancelled."
    return {
        "status": status,
        "label": STATUS_LABELS[status],
        "badge": STATUS_BADGE[status],
        "ahead": ahead,
        "message": message,
        "step": STEPS.index(status) if status in STEPS else -1,
    }

def form_context(form, errors):
    return dict(form=form, 
                errors=errors, 
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
    t = get_ticket(ticket_id)
    if t is None:
        abort(404)  # no ticket with that number
    return render_template("ticket.html", 
                           ticket=t, 
                           info=describe(t),
                           first_name=t["name"].split()[0],
                           updated=datetime.now().strftime("%I:%M %p").lstrip("0"))

@app.post("/queue/<int:ticket_id>/leave")
def leave(ticket_id):
    t = get_ticket(ticket_id)
    if t is None:
        abort(404)
    if t["status"] != "waiting":
        flash("Only a request that is still waiting can be cancelled.", "warning")
        return redirect(url_for("ticket", ticket_id=ticket_id))
    t["status"] = "cancelled"
    flash(f"Request #{ticket_id} was cancelled. You can send a new request anytime.", "info")
    return redirect(url_for("index"))

@app.get("/join")
def join_form():
    return render_template("join.html", **form_context({}, {}))

@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    color_mode = form.get("color_mode", "")
    copies = form.get("number_of_copies", type=int)
    paper_type = form.get("paper_type", "")
    paper_size = form.get("paper_size", "")
    notes = form.get("notes", "").strip()
    upload = request.files.get("file")

    errors = {}
    if not name:
        errors["name"] = "Enter your name."
    elif len(name) > 60:
        errors["name"] = "Keep your name under 60 characters."

    if upload is None or not upload.filename:
        errors["file"] = "Attach the PDF you want printed."
    elif not upload.filename.lower().endswith(".pdf"):
        errors["file"] = "Only PDF files are accepted. Save or export your file as a PDF first."
    elif upload.stream.read(5) != b"%PDF-":
        errors["file"] = "That file does not look like a valid PDF. Try exporting it again."
    else:
        upload.stream.seek(0)

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

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", **form_context(form, errors)), 400

    stored_name = f"{uuid.uuid4().hex}.pdf"
    upload.save(os.path.join(UPLOAD_DIR, stored_name))

    number = TICKETS[-1]["number"] + 1 if TICKETS else 1
    TICKETS.append({
        "number": number,
        "name": name,
        "service_id": SERVICES[0]["id"],
        "file_name": secure_filename(upload.filename) or "document.pdf",
        "file_path": f"uploads/{stored_name}",
        "number_of_copies": copies,
        "paper_size": paper_size,
        "paper_type": paper_type,
        "color_mode": color_mode,
        "notes": notes,
        "status": "waiting",
    })
    flash(f"Request submitted. Your ticket is #{number}.", "success")
    return redirect(url_for("ticket", ticket_id=number))

@app.errorhandler(RequestEntityTooLarge)
def too_large(_err):
    flash("That file is too large. The limit is 16 MB.", "danger")
    return render_template("join.html", **form_context({}, {"file": "Choose a PDF under 16 MB."})), 413

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.route("/staff")
def staff_dashboard():
    return "Staff dashboard coming soon"

if __name__ == "__main__":
    app.run(debug=True)
