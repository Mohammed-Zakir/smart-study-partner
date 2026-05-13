from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
from datetime import date, datetime
from pathlib import Path
import sqlite3
from routes.upload_routes import upload_bp
from routes.query_routes import query_bp
from routes.history_routes import history_bp
from routes.api_routes import api_bp
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# =====================
# DATABASE
# =====================

DB_NAME = "users.db"


def get_db_connection():

    conn = sqlite3.connect(DB_NAME)

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_db_connection()

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL
        )
        """
    )

    conn.commit()

    conn.close()


init_db()


# =====================
# USERS (can upgrade to DB later)
# =====================


# =====================
# LOGIN SYSTEM
# =====================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")

        password = request.form.get("password")

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()

        conn.close()

        if user:

            session["user"] = username

            return redirect(url_for("home"))

        return render_template(
            "login.html",
            error="Invalid credentials"
        )

    return render_template("login.html")
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")

        password = request.form.get("password")

        conn = get_db_connection()

        try:

            conn.execute(
                "INSERT INTO users(username,password) VALUES(?,?)",
                (username, password)
            )

            conn.commit()

            conn.close()

            return redirect(url_for("login"))

        except:

            conn.close()

            return render_template(
                "register.html",
                error="Username already exists"
            )

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


def require_login():
    return "user" in session
def get_progress_file():

    username = session.get("user", "guest")

    return Path(f"{username}_progress.json")

# =====================
# DATA HANDLING (UPGRADED)
# =====================

def default_data():
    return {
        "tasks": [],
        "streak": 0,
        "last_completed": None,
        "history": {}
    }


def load_data():

    progress_file = get_progress_file()

    try:

        if not progress_file.exists():

            return default_data()

        with open(progress_file, "r") as f:

            return json.load(f)

    except Exception as e:

        print("Load error:", e)

        return default_data()


def save_data(data):

    progress_file = get_progress_file()

    try:

        with open(progress_file, "w") as f:

            json.dump(data, f, indent=4)

    except Exception as e:

        print("Save error:", e)


# =====================
# DASHBOARD
# =====================

@app.route("/")
def home():
    if not require_login():
        return redirect(url_for("login"))

    return render_template("dashboard.html", user=session["user"])


# =====================
# PLAN GENERATION
# =====================

@app.route("/save_plan", methods=["POST"])
def save_plan():

    if not require_login():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}

    subjects = [
        s.strip()
        for s in data.get("subjects", [])
        if s.strip()
    ]

    toughest = data.get("toughest", "").strip()

    difficulty = data.get("difficulty", "Medium")

    hours = int(data.get("hours", 0))

    days = int(data.get("days", 0))

    progress = load_data()

    progress["tasks"] = []

    week_days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    for d in range(1, days + 1):

        total_subjects = len(subjects)

        remaining_hours = hours

        for i, s in enumerate(subjects):

            # BASE DISTRIBUTION
            sub_hours = max(1, hours // total_subjects)

            # TOUGH SUBJECT PRIORITY
            if s.lower() == toughest.lower():

                if difficulty == "Hard":
                    sub_hours += 2

                elif difficulty == "Medium":
                    sub_hours += 1

            # BALANCE REMAINING HOURS
            remaining_hours -= sub_hours

            if i == total_subjects - 1 and remaining_hours > 0:
                sub_hours += remaining_hours

            # TASK TYPE
            if d % 7 == 0:
                task_type = "Revision"
            else:
                task_type = "Practice"

            # PRIORITY
            if s.lower() == toughest.lower():
                priority = "High"
            else:
                priority = "Medium"

            progress["tasks"].append({

                "day": week_days[(d - 1) % 7],

                "subject": s,

                "hours": sub_hours,

                "type": task_type,

                "priority": priority,

                "difficulty": difficulty,

                "completed": False,

                "sessions_completed": 0,

                "created_at": datetime.now().isoformat()
            })

    save_data(progress)

    return jsonify({"ok": True})

# =====================
# ADD TASK
# =====================
@app.route("/toggle_by_time", methods=["POST"])
def toggle_by_time():

    if not require_login():
        return jsonify({"error":"Unauthorized"}), 401

    created_at = request.json.get("created_at")

    data = load_data()

    for task in data["tasks"]:

        if task["created_at"] == created_at:

            task["completed"] = not task["completed"]

            save_data(data)

            return jsonify({"ok":True})

    return jsonify({"error":"Task not found"}), 404

@app.route("/add_task", methods=["POST"])
def add_task():
    if not require_login():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    progress = load_data()

    progress["tasks"].append({
        "day": data.get("day", "Custom"),
        "subject": data.get("subject"),
        "hours": data.get("hours", 1),
        "priority": data.get("priority", "Medium"),
        "completed": False,
        "sessions_completed": 0,
        "created_at": datetime.now().isoformat()
    })

    save_data(progress)
    return jsonify({"ok": True})


# =====================
# DELETE TASK
# =====================

@app.route("/delete_task", methods=["POST"])
def delete_task():
    if not require_login():
        return jsonify({"error": "Unauthorized"}), 401

    idx = request.json.get("index")

    data = load_data()

    if 0 <= idx < len(data["tasks"]):
        data["tasks"].pop(idx)
        save_data(data)
        return jsonify({"ok": True})

    return jsonify({"error": "Invalid index"}), 400


# =====================
# PROGRESS (UPGRADED)
# =====================
def generate_timetable(tasks):

    timetable = []

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    slots = [
        "Morning",
        "Afternoon",
        "Evening"
    ]

    task_index = 0

    for day in days:

        row = {
            "day": day,
            "slots": []
        }

        for slot in slots:

            if task_index < len(tasks):

                t = tasks[task_index]

                row["slots"].append({

                    "subject":
                    t["subject"],

                    "type":
                    t["type"],

                    "priority":
                    t["priority"],

                    "hours":
                    t["hours"]
                })

                task_index += 1

            else:

                row["slots"].append({

                    "subject":"Free",

                    "type":"Break",

                    "priority":"Low",

                    "hours":0
                })

        timetable.append(row)

    return timetable

@app.route("/get_progress")
def get_progress():
    if not require_login():
        return jsonify({"error": "Unauthorized"}), 401

    data = load_data()

    completed = sum(1 for t in data["tasks"] if t["completed"])
    total = len(data["tasks"])

    percent = int((completed / total) * 100) if total else 0

    return jsonify({

    "tasks": data["tasks"],

    "completed": completed,

    "total": total,

    "percent": percent,

    "streak": data["streak"],

    "efficiency": percent,

    "pending": total - completed,

    "timetable": generate_timetable(
        data["tasks"]
    )

})


# =====================
# TOGGLE TASK (SMART STREAK)
# =====================

@app.route("/toggle_task", methods=["POST"])
def toggle_task():
    if not require_login():
        return jsonify({"error": "Unauthorized"}), 401

    idx = request.json.get("index")

    data = load_data()

    if 0 <= idx < len(data["tasks"]):
        task = data["tasks"][idx]
        task["completed"] = not task["completed"]

        today = date.today().isoformat()

        if today not in data["history"]:
            data["history"][today] = {"completed": 0, "sessions": 0}

        completed_today = sum(1 for t in data["tasks"] if t["completed"])
        data["history"][today]["completed"] = completed_today

        data["history"][today]["sessions"] += 1

        # 🔥 SMART STREAK LOGIC
        if task["completed"]:
            last = data.get("last_completed")

            if last:
                diff = (date.today() - datetime.fromisoformat(last).date()).days
                if diff == 1:
                    data["streak"] += 1
                elif diff > 1:
                    data["streak"] = 1
            else:
                data["streak"] = 1

            data["last_completed"] = today

        save_data(data)
        return jsonify({"ok": True})

    return jsonify({"error": "Invalid index"}), 400


# =====================
# STATS (SMOOTHER GRAPH)
# =====================
@app.route("/complete_session", methods=["POST"])
def complete_session():

    if not require_login():
        return jsonify({
            "error":"Unauthorized"
        }), 401

    data = load_data()

    tasks = data["tasks"]

    for task in tasks:

        # SKIP COMPLETED
        if task["completed"]:
            continue

        # SESSION INCREMENT
        task["sessions_completed"] += 1

        required_sessions = max(
            1,
            int(task["hours"])
        )

        # AUTO COMPLETE
        if (
            task["sessions_completed"]
            >= required_sessions
        ):

            task["completed"] = True

        # ONLY UPDATE ONE TASK
        break

    save_data(data)

    return jsonify({
        "ok":True
    })
@app.route("/stats")
def stats():
    if not require_login():
        return jsonify({"error": "Unauthorized"}), 401

    history = load_data().get("history", {})

    labels = []
    values = []

    for d, v in sorted(history.items()):
        labels.append(d[-5:])
        score = (v.get("completed", 0) * 2) + v.get("sessions", 0)
        values.append(score)

    return jsonify({
        "labels": labels[-10:],
        "values": values[-10:]
    })


# =====================
# SUBJECT ANALYTICS (UPGRADED)
# =====================

@app.route("/subject_stats")
def subject_stats():
    if not require_login():
        return jsonify({"error": "Unauthorized"}), 401

    tasks = load_data()["tasks"]

    summary = {}

    for t in tasks:
        sub = t["subject"]

        if sub not in summary:
            summary[sub] = {"completed": 0, "total": 0}

        summary[sub]["total"] += 1
        if t["completed"]:
            summary[sub]["completed"] += 1

    return jsonify(summary)


# =====================
# INSIGHTS (NEW COOL FEATURE)
# =====================

@app.route("/insights")
def insights():

    if not require_login():
        return jsonify({"error": "Unauthorized"}), 401

    data = load_data()

    tasks = data["tasks"]

    completed = sum(1 for t in tasks if t["completed"])

    total = len(tasks)

    if total == 0:
        msg = "Create your first AI study plan 🚀"

    else:

        subject_stats = {}

        for t in tasks:

            sub = t["subject"]

            if sub not in subject_stats:
                subject_stats[sub] = {
                    "completed":0,
                    "total":0
                }

            subject_stats[sub]["total"] += 1

            if t["completed"]:
                subject_stats[sub]["completed"] += 1

        weakest = None
        lowest = 999

        for sub, stats in subject_stats.items():

            percent = (
                stats["completed"] /
                stats["total"]
            ) * 100

            if percent < lowest:
                lowest = percent
                weakest = sub

        if completed == total:

            msg = (
                "Excellent consistency! "
                "All study goals completed 🔥"
            )

        elif completed > total / 2:

            msg = (
                f"Good progress overall. "
                f"Focus more on {weakest} practice."
            )

        else:

            msg = (
                f"Your completion rate is low. "
                f"Prioritize {weakest} and maintain consistency."
            )

    return jsonify({"message": msg})


# =====================
# BLUEPRINTS
# =====================

app.register_blueprint(upload_bp)
app.register_blueprint(query_bp)
app.register_blueprint(history_bp)
app.register_blueprint(api_bp)


# =====================
# RUN
# =====================

if __name__ == "__main__":
    app.run(debug=True)