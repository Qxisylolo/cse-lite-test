import os
import pickle
from flask import Flask, request, redirect, make_response

app = Flask(__name__)


JWT_SECRET = "my-super-secret-key-12345"


@app.route("/search")
def search():
    query = request.args.get("q", "")
    return f"<h1>Results for: {query}</h1>"

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
    f = request.files["file"]
    f.save(f"/var/www/uploads/{f.filename}")
    return "Uploaded"

@app.route("/deserialize", methods=["POST"])
def deserialize():
    data = request.get_data()
    obj = pickle.loads(data)
    return str(obj)


@app.route("/exec", methods=["POST"])
def execute_code():
    expr = request.form.get("expression", "0")
    result = eval(expr)
    return str(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")