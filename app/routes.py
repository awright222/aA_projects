import os
import sqlite3
from flask import Blueprint, render_template, redirect, url_for
from datetime import datetime
from .forms import AppointmentForm

bp = Blueprint('main', __name__, url_prefix='/')
DB_FILE = os.environ.get("DB_FILE")

@bp.route("/", methods=["GET", "POST"])
def main():
    form = AppointmentForm()
    if form.validate_on_submit():
        params = {
            'name': form.name.data,
            'start_datetime': datetime.combine(form.start_date.data, form.start_time.data),
            'end_datetime': datetime.combine(form.end_date.data, form.end_time.data),
            'description': form.description.data,
            'private': form.private.data
        }
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO appointments (name, start_datetime, end_datetime, description, private)
            VALUES (:name, :start_datetime, :end_datetime, :description, :private)
        """, params)
        conn.commit()
        conn.close()
        return redirect(url_for('main.main'))

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