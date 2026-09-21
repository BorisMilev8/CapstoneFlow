def test_login_page_loads(client):
    response = client.get("/login")

    assert response.status_code == 200
    assert b"Sign in" in response.data
    assert b"student@capstoneflow.local" in response.data


def test_dashboard_requires_login(client):
    response = client.get("/dashboard")

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")


def test_student_can_sign_in(client):
    response = client.post(
        "/login",
        data={
            "email": "student@capstoneflow.local",
            "password": "Student123!",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"CapstoneFlow" in response.data
    assert b"Student workspace" in response.data
    assert b"75%" in response.data


def test_reviewer_role_is_session_backed(client):
    response = client.post(
        "/login",
        data={
            "email": "reviewer@capstoneflow.local",
            "password": "Reviewer123!",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Reviewer workspace" in response.data


def test_invalid_password_is_rejected(client):
    response = client.post(
        "/login",
        data={
            "email": "student@capstoneflow.local",
            "password": "wrong-password",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Email or password is incorrect." in response.data


def test_logout_clears_session(client):
    client.post(
        "/login",
        data={
            "email": "student@capstoneflow.local",
            "password": "Student123!",
        },
    )

    response = client.post("/logout", follow_redirects=True)

    assert response.status_code == 200
    assert b"Sign in" in response.data

    protected = client.get("/dashboard")
    assert protected.status_code == 302
