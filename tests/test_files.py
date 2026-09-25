from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_token():
    login_response = client.post(
        "/auth/login",
        json={
            "username": "sriharini",
            "password": "password123"
        }
    )

    assert login_response.status_code == 200

    return login_response.json()["access_token"]


def test_file_upload():

    token = get_token()

    file_content = b"%PDF-1.4 test file content"

    response = client.post(
        "/files/upload",
        headers={
            "Authorization": f"Bearer {token}"
        },
        files={
            "file": (
                "test.pdf",
                file_content,
                "application/pdf"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "File uploaded successfully"
    assert data["uploaded_by"] == "sriharini"


def test_invalid_file_type():

    token = get_token()

    response = client.post(
        "/files/upload",
        headers={
            "Authorization": f"Bearer {token}"
        },
        files={
            "file": (
                "malicious.exe",
                b"fake executable content",
                "application/octet-stream"
            )
        }
    )

    assert response.status_code == 400

    assert response.json()["detail"] == "File type not allowed"