import pytest

from app import create_app


@pytest.fixture()
def app(tmp_path):
    database_path = tmp_path / "capstoneflow-test.sqlite3"

    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "DATABASE": str(database_path),
        }
    )
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def student_login(client):
    response = client.post(
        "/login",
        data={
            "email": "student@capstoneflow.local",
            "password": "Student123!",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    return client


@pytest.fixture()
def reviewer_login(client):
    response = client.post(
        "/login",
        data={
            "email": "reviewer@capstoneflow.local",
            "password": "Reviewer123!",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    return client
