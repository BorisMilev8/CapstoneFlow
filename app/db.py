import sqlite3
from pathlib import Path

import click
from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")

    return g.db


def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    schema_path = Path(__file__).with_name("schema.sql")

    with schema_path.open("r", encoding="utf-8") as schema_file:
        db.executescript(schema_file.read())

    count = db.execute("SELECT COUNT(*) FROM requirements").fetchone()[0]
    if count == 0:
        seed_requirements(db)

    db.commit()


def seed_requirements(db):
    rows = [
        (
            "R1",
            "Create and edit a project profile",
            "Keep project title, scope, and contacts in one place.",
            "Student can create or update the project profile and saved values persist.",
            "Alpha",
            "Must",
            "Complete",
            1,
            "https://example.org/r1",
            0,
            0,
        ),
        (
            "R2",
            "View requirements by checkpoint",
            "Make checkpoint-specific scope visible to the student and reviewer.",
            "User can filter requirements by checkpoint and see the correct stored records.",
            "Alpha",
            "Must",
            "Complete",
            1,
            "https://example.org/r2",
            0,
            0,
        ),
        (
            "R3",
            "Prioritize user stories with acceptance criteria",
            "Store planned work with priority and testable acceptance criteria.",
            "Student can create and edit a requirement with checkpoint, priority, and acceptance criteria.",
            "Alpha",
            "Must",
            "Complete",
            1,
            "",
            1,
            0,
        ),
        (
            "R4",
            "Assigned reviewer can inspect scope and requirements",
            "Allow the assigned reviewer to inspect the current project plan.",
            "Reviewer can open the requirement list and inspect stored requirement details.",
            "Alpha",
            "Must",
            "Complete",
            1,
            "https://example.org/r4",
            0,
            0,
        ),
    ]

    db.executemany(
        """
        INSERT INTO requirements (
            code, title, description, acceptance_criteria, checkpoint,
            priority, status, required, evidence_url,
            blocking_feedback, overdue
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )


@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Initialized the CapstoneFlow database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
