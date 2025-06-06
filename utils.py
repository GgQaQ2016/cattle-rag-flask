from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import session, redirect, url_for


def hash_password(password: str) -> str:
    """Return a hashed version of the password."""
    return generate_password_hash(password)


def verify_password(pw_hash: str, password: str) -> bool:
    """Verify a password against its hash."""
    return check_password_hash(pw_hash, password)


def login_required(view):
    """Simple decorator to ensure a user is logged in."""

    @wraps(view)
    def wrapped_view(**kwargs):
        if not session.get("user_id"):
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view
