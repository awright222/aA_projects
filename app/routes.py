import os
import sqlite3
from flask import Blueprint, render_template
from datetime import datetime
from .forms.py import AppointmentForm

bp = Blueprint('main', __name__, url_prefix='/')
DB_FILE = os.environ.get("DB_FILE")

@bp.route("/", methods=["GET", "POST"])
def main():
    form = AppointmentForm()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, start_datetime, end_datetime
        FROM appointments
        ORDER BY start_datetime;
    """)
    rows = cursor.fetchall()
    conn.close()

    # Convert datetime strings to datetime objects
    appointments = []
    for row in rows:
        id, name, start_datetime, end_datetime = row
        start_datetime = datetime.strptime(start_datetime, '%Y-%m-%d %H:%M:%S')
        end_datetime = datetime.strptime(end_datetime, '%Y-%m-%d %H:%M:%S')
        appointments.append((id, name, start_datetime, end_datetime))

    return render_template("main.html", appointments=appointments, form=form)