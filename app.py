"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-me"  # Week 11 moves this into an environment variable

SERVICES = [
    {"id": 1, "name": "Document Printing"},
]

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
        "color_mode": "Black and White",
        "status": "waiting",
    },
    {
        "number": 2,
        "name": "Lex Ian",
        "email": "lexian@gmail.com",
        "service_id": 1,
        "file_name": "report.pdf",
        "file_path": "uploads/report.pdf",
        "number_of_copies": 1,
        "paper_size": "Long",
        "paper_type": "Bond Paper",
        "color_mode": "Colored",
        "status": "printing",
    },
]


@app.route("/")
def index():
    # render_template looks inside the templates/ folder and passes
    # keyword arguments to the template as variables.
    return render_template("index.html")

@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    # <int:ticket_id> only matches numbers, so /queue/abc returns 404.
    for position, t in enumerate(TICKETS, start=1):
        if t["number"] == ticket_id:
            return render_template("ticket.html", ticket=t, position=position)
    abort(404)  # no ticket with that number

@app.route("/join")
def join_form():
    return render_template("join.html")

@app.route("/staff")
def staff_dashboard():
    return "Staff dashboard coming soon"

if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
