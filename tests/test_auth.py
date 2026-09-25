from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200

    assert response.json()["message"] == "Secure Student API is running"


def test_invalid_login():
    response = client.post(
        "/auth/login",
        json={
            "username": "wrong_user",
            "password": "wrong_password"
        }
    )

    assert response.status_code == 401


def test_student_cannot_access_admin():

    # Login as student
    login_response = client.post(
        "/auth/login",
        json={
            "username": "sriharini",
            "password": "password123"
        }
    )

    assert login_response.status_code == 200

    # Get JWT token
    token = login_response.json()["access_token"]

    # Try to access admin endpoint
    response = client.get(
        "/admin/users",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    # Student should not be allowed
    assert response.status_code == 403