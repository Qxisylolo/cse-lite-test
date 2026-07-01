"""Simple API server with multiple security vulnerabilities."""

import os
import pickle
import yaml
from flask import Flask, request, redirect, make_response

app = Flask(__name__)

# Hardcoded JWT secret
JWT_SECRET = "my-super-secret-key-12345"


@app.route("/search")
def search():
    """XSS: user input reflected directly in HTML response."""
    query = request.args.get("q", "")
    return f"<h1>Results for: {query}</h1>"


@app.route("/redirect")
def open_redirect():
    """Open redirect: no validation on redirect target."""
    url = request.args.get("url", "/")
    return redirect(url)


@app.route("/deserialize", methods=["POST"])
def deserialize():
    """Insecure deserialization: pickle.loads on user input."""
    data = request.get_data()
    obj = pickle.loads(data)
    return str(obj)


@app.route("/config")
def load_config():
    """Unsafe YAML: yaml.load without SafeLoader allows code execution."""
    config_data = request.args.get("data", "")
    config = yaml.load(config_data)
    return str(config)


@app.route("/exec", methods=["POST"])
def execute_code():
    """Code injection: eval on user-supplied expression."""
    expr = request.form.get("expression", "0")
    result = eval(expr)
    return str(result)


@app.route("/login", methods=["POST"])
def login():
    """Timing attack: string comparison leaks password length."""
    password = request.form.get("password", "")
    correct = os.environ.get("ADMIN_PASSWORD", "admin123")
    if password == correct:
        resp = make_response("OK")
        # Insecure cookie: no httponly, no secure flag
        resp.set_cookie("session", "admin", httponly=False, secure=False)
        return resp
    return "Unauthorized", 401


@app.route("/upload", methods=["POST"])
def upload():
    """Unrestricted file upload: no extension or content-type validation."""
    f = request.files["file"]
    f.save(f"/var/www/uploads/{f.filename}")
    return "Uploaded"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
