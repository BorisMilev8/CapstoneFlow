from functools import wraps

from flask import redirect, session, url_for


def login_required(view):
    """Require a signed-in CapstoneFlow session for protected routes."""

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_email" not in session:
            return redirect(url_for("main.login"))
        return view(*args, **kwargs)

    return wrapped_view
