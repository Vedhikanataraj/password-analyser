from flask import Flask, render_template, request
from analyzer import evaluate_password, suggest_password
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DB_FILE = "passwords.db"

# --- DATABASE LOGIC ---
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS password_history (id INTEGER PRIMARY KEY, pwhash TEXT)")
        conn.commit()

def is_password_reused(new_password):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT pwhash FROM password_history")
        for row in cursor.fetchall():
            if check_password_hash(row[0], new_password):
                return True
    return False

def save_password(password):
    hashed = generate_password_hash(password)
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO password_history (pwhash) VALUES (?)", (hashed,))
        conn.commit()

init_db()

# --- WEB ROUTES ---
@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    password_input = ""
    error_msg = None
    
    if request.method == "POST":
        password_input = request.form.get("password")
        if password_input:
            if is_password_reused(password_input):
                error_msg = "SECURITY ALERT: You have used this password before. Please choose a new one."
            else:
                result = evaluate_password(password_input)
                if result['strength'] == "Strong":
                    save_password(password_input)
            
    return render_template("index.html", result=result, password=password_input, suggestion=suggest_password(), error_msg=error_msg)

if __name__ == "__main__":
    app.run(debug=True)