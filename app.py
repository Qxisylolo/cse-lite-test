import sqlite3
import os
import subprocess


def get_user(user_id):
    """SQL injection: user input directly in query string."""
    conn = sqlite3.connect("users.db")
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return conn.execute(query).fetchone()


def run_command(user_input):
    """Command injection: user input passed directly to shell."""
    result = subprocess.run(f"echo {user_input}", shell=True, capture_output=True)
    return result.stdout


def read_file(filename):
    """Path traversal: no sanitization on user-provided filename."""
    path = f"/data/uploads/{filename}"
    with open(path) as f:
        return f.read()


# Hardcoded credentials
API_KEY = "sk-1234567890abcdef"
DATABASE_PASSWORD = "super_secret_password_123"
AWS_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
