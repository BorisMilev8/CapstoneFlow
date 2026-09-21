from app.db import get_db


def test_requirements_page_requires_login(client):
    response = client.get("/requirements")

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")


def test_student_can_view_seeded_requirements(student_login):
    response = student_login.get("/requirements")

    assert response.status_code == 200
    assert b"Requirements workspace" in response.data
    assert b"R1" in response.data
    assert b"R4" in response.data


def test_student_can_create_requirement(student_login, app):
    response = student_login.post(
        "/requirements/new",
        data={
            "code": "R5",
            "title": "Submit a weekly status report",
            "description": "Record project progress each week.",
            "acceptance_criteria": "A saved report can be reviewed after submission.",
            "checkpoint": "Alpha",
            "priority": "Must",
            "status": "Planned",
            "required": "on",
            "evidence_url": "",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Requirement created and saved to SQLite." in response.data
    assert b"R5" in response.data

    with app.app_context():
        saved = get_db().execute(
            "SELECT * FROM requirements WHERE code = 'R5'"
        ).fetchone()
        assert saved is not None
        assert saved["priority"] == "Must"
        assert saved["checkpoint"] == "Alpha"


def test_student_can_edit_r3_and_dashboard_recalculates(student_login, app):
    with app.app_context():
        r3 = get_db().execute(
            "SELECT * FROM requirements WHERE code = 'R3'"
        ).fetchone()
        requirement_id = r3["id"]

    response = student_login.post(
        f"/requirements/{requirement_id}/edit",
        data={
            "code": "R3",
            "title": "Prioritize user stories with acceptance criteria",
            "description": "Store planned work with priority and testable acceptance criteria.",
            "acceptance_criteria": "Student can create and edit requirements with persistent fields.",
            "checkpoint": "Alpha",
            "priority": "Must",
            "status": "Complete",
            "required": "on",
            "evidence_url": "https://example.org/r3-test",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Requirement changes saved." in response.data

    dashboard = student_login.get("/dashboard")
    assert dashboard.status_code == 200
    assert b"100%" in dashboard.data
    assert b"All required Alpha items are ready." in dashboard.data


def test_reviewer_can_view_but_cannot_create(reviewer_login):
    list_response = reviewer_login.get("/requirements")
    create_response = reviewer_login.get("/requirements/new")

    assert list_response.status_code == 200
    assert b"Read-only reviewer view" in list_response.data
    assert create_response.status_code == 403


def test_checkpoint_filter_uses_stored_values(student_login):
    response = student_login.get("/requirements?checkpoint=Beta")

    assert response.status_code == 200
    assert b"No requirements match these filters." in response.data
