from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "test_key"

db = "game.db"


def get_db():
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INT,
        minutes INT,
        coins INT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


def require_login():
    if "user_id" not in session:
        return False
    return True


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=?", (username,)
        ).fetchone()

        if not user:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password),
            )
            conn.commit()

            user = conn.execute(
                "SELECT * FROM users WHERE username=?", (username,)
            ).fetchone()

        if user["password"] == password:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            conn.close()
            return redirect(url_for("index"))

        conn.close()

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
def index():
    if not require_login():
        return redirect(url_for("login"))

    if request.method == "POST":
        mins = int(request.form["minutes"])
        coins = mins // 5

        conn = get_db()
        conn.execute(
            "INSERT INTO sessions (user_id, minutes, coins, created_at) VALUES (?, ?, ?, ?)",
            (session["user_id"], mins, coins, datetime.now().isoformat()),
        )
        conn.commit()
        conn.close()

        # TODO: add sessions
        return redirect(url_for("sessions"))

    return render_template("index.html", username=session["username"])
