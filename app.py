from flask import Flask, render_template, request, redirect, session
import sqlite3, uuid

app = Flask(__name__)
app.secret_key = "tedx_secret"

PRICE = 1000
ADMIN_USER = "admin"
ADMIN_PASS = "tedx123"

# ---------- DATABASE ----------
def get_db():
    return sqlite3.connect("bookings.db")

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT,
            name TEXT,
            phone TEXT,
            email TEXT,
            school TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------- USER ROUTES ----------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ticket")
def ticket():
    return render_template("tickets.html")

@app.route("/book", methods=["POST"])
def book():
    names = request.form.getlist("name[]")
    phones = request.form.getlist("phone[]")
    emails = request.form.getlist("email[]")
    school = request.form["school"]

    ticket_id = "TEDX-" + str(uuid.uuid4())[:8].upper()

    conn = get_db()
    cur = conn.cursor()
    for i in range(len(names)):
        cur.execute("""
            INSERT INTO bookings (ticket_id, name, phone, email, school)
            VALUES (?, ?, ?, ?, ?)
        """, (ticket_id, names[i], phones[i], emails[i], school))
    conn.commit()
    conn.close()

    total = len(names) * PRICE
    return render_template("success.html",
                           ticket_id=ticket_id,
                           names=names,
                           school=school,
                           qty=len(names),
                           total=total)

# ---------- ADMIN LOGIN ----------
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form["username"] == ADMIN_USER and request.form["password"] == ADMIN_PASS:
            session["admin"] = True
            return redirect("/dashboard")
    return render_template("admin_login.html")

# ---------- ADMIN DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect("/admin")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM bookings")
    data = cur.fetchall()

    total_tickets = len(data)
    total_amount = total_tickets * PRICE

    conn.close()

    return render_template("admin_dashboard.html",
                           data=data,
                           total_tickets=total_tickets,
                           total_amount=total_amount)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/admin")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

