from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_students_without_token():
    response = client.get("/students/")

    assert response.status_code == 401


def test_admin_without_token():
    response = client.get("/admin/dashboard")

    assert response.status_code == 401