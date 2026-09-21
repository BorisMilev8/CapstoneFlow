from werkzeug.security import generate_password_hash


DEMO_USERS = {
    "student@capstoneflow.local": {
        "display_name": "Demo Student",
        "role": "Student",
        "password_hash": generate_password_hash("Student123!"),
    },
    "reviewer@capstoneflow.local": {
        "display_name": "Demo Reviewer",
        "role": "Reviewer",
        "password_hash": generate_password_hash("Reviewer123!"),
    },
}


PROJECT = {
    "title": "CapstoneFlow",
    "checkpoint": "Alpha",
    "semester": "Fall 2026",
}


CHECKPOINT_ITEMS = [
    {
        "id": "R1",
        "title": "Create and edit a project profile",
        "status": "Complete",
        "required": True,
        "evidence_links": ["https://example.org/r1"],
        "open_blocking_feedback": False,
        "overdue": False,
    },
    {
        "id": "R2",
        "title": "View requirements by checkpoint",
        "status": "Complete",
        "required": True,
        "evidence_links": ["https://example.org/r2"],
        "open_blocking_feedback": False,
        "overdue": False,
    },
    {
        "id": "R3",
        "title": "Prioritize user stories with acceptance criteria",
        "status": "Complete",
        "required": True,
        "evidence_links": [],
        "open_blocking_feedback": True,
        "overdue": False,
    },
    {
        "id": "R4",
        "title": "Assigned reviewer can inspect scope and requirements",
        "status": "Complete",
        "required": True,
        "evidence_links": ["https://example.org/r4"],
        "open_blocking_feedback": False,
        "overdue": False,
    },
]
