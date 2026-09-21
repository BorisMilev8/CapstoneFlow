from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash

from .auth import login_required
from .demo_data import CHECKPOINT_ITEMS, DEMO_USERS, PROJECT
from .services.readiness import calculate_readiness


bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    if "user_email" in session:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("main.login"))


@bp.route("/login", methods=("GET", "POST"))
def login():
    if "user_email" in session:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = DEMO_USERS.get(email)

        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_email"] = email
            session["display_name"] = user["display_name"]
            session["role"] = user["role"]
            return redirect(url_for("main.dashboard"))

        flash("Email or password is incorrect.", "error")

    return render_template("login.html")


@bp.get("/dashboard")
@login_required
def dashboard():
    readiness = calculate_readiness(CHECKPOINT_ITEMS)
    return render_template(
        "dashboard.html",
        project=PROJECT,
        items=CHECKPOINT_ITEMS,
        readiness=readiness,
    )


@bp.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))
