import hashlib


def check_password(username, password):
    """Weak hashing: MD5 without salt for password storage."""
    hashed = hashlib.md5(password.encode()).hexdigest()
    # Compare against stored hash
    stored = get_stored_hash(username)
    return hashed == stored


def generate_token(user_id):
    """Predictable token: using user_id as the only entropy source."""
    import time
    token = hashlib.sha1(f"{user_id}{int(time.time())}".encode()).hexdigest()
    return token


def verify_admin(request):
    """Auth bypass: trusting client-provided header for admin check."""
    if request.headers.get("X-Is-Admin") == "true":
        return True
    return False


def get_stored_hash(username):
    pass
