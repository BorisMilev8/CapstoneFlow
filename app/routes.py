import sqlite3

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash

from .auth import login_required, role_required
from .db import get_db
from .demo_data import DEMO_USERS, PROJECT
from .services.readiness import calculate_readiness


bp = Blueprint("main", __name__)

CHECKPOINTS = ("Proposal", "Alpha", "Beta", "Final")
PRIORITIES = ("Must", "Should", "Could")
STATUSES = ("Planned", "In progress", "Complete")


def row_to_readiness_item(row):
    evidence = row["evidence_url"].strip()
    return {
        "id": row["code"],
        "db_id": row["id"],
        "title": row["title"],
        "status": row["status"],
        "required": bool(row["required"]),
        "evidence_links": [evidence] if evidence else [],
        "open_blocking_feedback": bool(row["blocking_feedback"]),
        "overdue": bool(row["overdue"]),
    }


def get_requirement(requirement_id):
    requirement = get_db().execute(
        "SELECT * FROM requirements WHERE id = ?",
        (requirement_id,),
    ).fetchone()

    if requirement is None:
        abort(404)

    return requirement


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
    rows = get_db().execute(
        """
        SELECT *
        FROM requirements
        WHERE checkpoint = ?
        ORDER BY
            CASE priority
                WHEN 'Must' THEN 1
                WHEN 'Should' THEN 2
                ELSE 3
            END,
            code
        """,
        (PROJECT["checkpoint"],),
    ).fetchall()

    items = [row_to_readiness_item(row) for row in rows]
    readiness = calculate_readiness(items)

    next_attention = next(
        (
            item
            for item in items
            if not (
                item["status"] == "Complete"
                and item["evidence_links"]
                and not item["open_blocking_feedback"]
            )
        ),
        None,
    )

    return render_template(
        "dashboard.html",
        project=PROJECT,
        items=items,
        readiness=readiness,
        next_attention=next_attention,
    )


@bp.get("/requirements")
@login_required
def requirements():
    checkpoint = request.args.get("checkpoint", "").strip()
    priority = request.args.get("priority", "").strip()

    query = "SELECT * FROM requirements WHERE 1 = 1"
    params = []

    if checkpoint in CHECKPOINTS:
        query += " AND checkpoint = ?"
        params.append(checkpoint)

    if priority in PRIORITIES:
        query += " AND priority = ?"
        params.append(priority)

    query += """
        ORDER BY
            CASE checkpoint
                WHEN 'Proposal' THEN 1
                WHEN 'Alpha' THEN 2
                WHEN 'Beta' THEN 3
                ELSE 4
            END,
            CASE priority
                WHEN 'Must' THEN 1
                WHEN 'Should' THEN 2
                ELSE 3
            END,
            code
    """

    rows = get_db().execute(query, params).fetchall()

    return render_template(
        "requirements.html",
        requirements=rows,
        checkpoints=CHECKPOINTS,
        priorities=PRIORITIES,
        selected_checkpoint=checkpoint,
        selected_priority=priority,
    )


@bp.route("/requirements/new", methods=("GET", "POST"))
@role_required("Student")
def requirement_create():
    if request.method == "POST":
        error = save_requirement_from_form()

        if error is None:
            flash("Requirement created and saved to SQLite.", "success")
            return redirect(url_for("main.requirements"))

        flash(error, "error")

    return render_template(
        "requirement_form.html",
        requirement=None,
        checkpoints=CHECKPOINTS,
        priorities=PRIORITIES,
        statuses=STATUSES,
        form_title="Create requirement",
    )


@bp.route("/requirements/<int:requirement_id>/edit", methods=("GET", "POST"))
@role_required("Student")
def requirement_edit(requirement_id):
    requirement = get_requirement(requirement_id)

    if request.method == "POST":
        error = save_requirement_from_form(requirement_id)

        if error is None:
            flash("Requirement changes saved.", "success")
            return redirect(url_for("main.requirements"))

        flash(error, "error")

    requirement = get_requirement(requirement_id)

    return render_template(
        "requirement_form.html",
        requirement=requirement,
        checkpoints=CHECKPOINTS,
        priorities=PRIORITIES,
        statuses=STATUSES,
        form_title=f"Edit {requirement['code']}",
    )


def save_requirement_from_form(requirement_id=None):
    code = request.form.get("code", "").strip().upper()
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    acceptance_criteria = request.form.get("acceptance_criteria", "").strip()
    checkpoint = request.form.get("checkpoint", "")
    priority = request.form.get("priority", "")
    status = request.form.get("status", "")
    evidence_url = request.form.get("evidence_url", "").strip()
    required = 1 if request.form.get("required") == "on" else 0
    blocking_feedback = 1 if request.form.get("blocking_feedback") == "on" else 0
    overdue = 1 if request.form.get("overdue") == "on" else 0

    if not code:
        return "Requirement ID is required."
    if not title:
        return "Requirement title is required."
    if not acceptance_criteria:
        return "Acceptance criteria are required."
    if checkpoint not in CHECKPOINTS:
        return "Choose a valid checkpoint."
    if priority not in PRIORITIES:
        return "Choose a valid priority."
    if status not in STATUSES:
        return "Choose a valid status."

    db = get_db()

    try:
        if requirement_id is None:
            db.execute(
                """
                INSERT INTO requirements (
                    code, title, description, acceptance_criteria,
                    checkpoint, priority, status, required,
                    evidence_url, blocking_feedback, overdue
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    code,
                    title,
                    description,
                    acceptance_criteria,
                    checkpoint,
                    priority,
                    status,
                    required,
                    evidence_url,
                    blocking_feedback,
                    overdue,
                ),
            )
        else:
            db.execute(
                """
                UPDATE requirements
                SET
                    code = ?,
                    title = ?,
                    description = ?,
                    acceptance_criteria = ?,
                    checkpoint = ?,
                    priority = ?,
                    status = ?,
                    required = ?,
                    evidence_url = ?,
                    blocking_feedback = ?,
                    overdue = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    code,
                    title,
                    description,
                    acceptance_criteria,
                    checkpoint,
                    priority,
                    status,
                    required,
                    evidence_url,
                    blocking_feedback,
                    overdue,
                    requirement_id,
                ),
            )
        db.commit()
    except sqlite3.IntegrityError:
        return f"Requirement ID {code} already exists."

    return None


@bp.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))
