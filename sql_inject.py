import sqlite3
from flask import Flask, request, redirect, make_response

app = Flask(__name__)

@app.route("/user")
def get_user():
    user_id = request.args.get("id", "")
    conn = sqlite3.connect("app.db")
    cursor = conn.execute(f"SELECT * FROM users WHERE id = '{user_id}'")
    result = cursor.fetchone()
    conn.close()
    return str(result)
