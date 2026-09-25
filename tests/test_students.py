from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_students_without_token():
    response = client.get("/students/")

    assert response.status_code == 401


def test_students_with_token():
    # Login with an existing user
    login_response = client.post(
        "/auth/login",
        json={
            "username": "sriharini",
            "password": "password123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Access protected student endpoint
    response = client.get(
        "/students/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "sriharini"
    assert data["role"] == "student"