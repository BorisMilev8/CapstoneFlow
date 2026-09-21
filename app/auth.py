from functools import wraps

from flask import abort, redirect, session, url_for


def login_required(view):
    """Require a signed-in CapstoneFlow session for protected routes."""

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_email" not in session:
            return redirect(url_for("main.login"))
        return view(*args, **kwargs)

    return wrapped_view


def role_required(*allowed_roles):
    """Require the signed-in user to have one of the supplied roles."""

    def decorator(view):
        @wraps(view)
        @login_required
        def wrapped_view(*args, **kwargs):
            if session.get("role") not in allowed_roles:
                abort(403)
            return view(*args, **kwargs)

        return wrapped_view

    return decorator
