# Secure Student API

A FastAPI backend for student-management workflows with JWT authentication, role-based access control (RBAC), PostgreSQL persistence, and protected file uploads.

## Features

- User registration and login with bcrypt password hashing
- JWT access tokens with a 30-minute lifetime
- Student and admin roles
- Protected student endpoints
- Admin-only dashboard and user endpoints
- Authenticated file uploads with extension and size validation
- Automatic request and response logging
- Interactive API documentation through Swagger UI and ReDoc

## Tech Stack

- Python 3.12
- FastAPI and Uvicorn
- SQLAlchemy
- PostgreSQL
- Passlib with bcrypt
- PyJWT
- Pytest

## Project Structure

```text
.
├── app/
│   ├── main.py              # FastAPI application and middleware
│   ├── config.py            # JWT configuration
│   ├── database.py          # SQLAlchemy engine and sessions
│   ├── auth_utils.py        # Authentication helpers
│   ├── models/              # Database models
│   ├── routers/             # Auth, student, admin, and file routes
│   ├── schemas/             # Request schemas
│   └── services/             # Authentication and authorization logic
├── tests/                   # API and RBAC tests
├── create_admin.py          # Creates or promotes an admin account
├── Dockerfile
├── requirements.txt
└── uploads/                 # Uploaded files
```

## Prerequisites

- Python 3.12 or later
- PostgreSQL 12 or later
- A PostgreSQL database and connection URL

## Local Setup

1. Create and activate a virtual environment:

	```powershell
	python -m venv venv
	.\venv\Scripts\Activate.ps1
	```

	On macOS or Linux:

	```bash
	python -m venv venv
	source venv/bin/activate
	```

2. Install dependencies:

	```bash
	pip install -r requirements.txt
	```

3. Create a `.env` file in the project root:

	```dotenv
	SECRET_KEY=replace-with-a-long-random-secret
	DATABASE_URL=postgresql://username:password@localhost:5432/secure_student_db
	```

	Use a strong, private value for `SECRET_KEY`. Do not commit `.env` or production credentials.

4. Start the API:

	```bash
	uvicorn app.main:app --reload
	```

	The API is available at `http://127.0.0.1:8000`.

## Docker

Build and run the application container:

```bash
docker build -t secure-student-api .
docker run --name secure-student-api -p 8000:8000 \
  -e SECRET_KEY=replace-with-a-long-random-secret \
  -e DATABASE_URL=postgresql://username:password@host.docker.internal:5432/secure_student_db \
  secure-student-api
```

The container expects PostgreSQL to be available through the `DATABASE_URL` environment variable. The Docker image creates `uploads/` and `logs/` inside the container; mount persistent volumes if those files must survive container replacement.

## Create an Admin User

After configuring the database, run:

```bash
python create_admin.py
```

This creates the `admin` account with the credentials defined by the script, or promotes an existing `admin` user. Change any default credentials immediately in a real deployment and consider replacing this one-off script with a managed provisioning process.

## API Usage

### Health check

```http
GET /
```

### Register a student

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"student1","email":"student1@example.com","password":"strong-password"}'
```

New registrations receive the `student` role.

### Log in

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"student1","password":"strong-password"}'
```

The response contains an access token. Send it on protected requests as:

```text
Authorization: Bearer <access-token>
```

### Available routes

| Method | Route | Access |
| --- | --- | --- |
| `GET` | `/` | Public health check |
| `POST` | `/auth/register` | Public |
| `POST` | `/auth/login` | Public |
| `GET` | `/students/` | Authenticated users |
| `GET` | `/admin/dashboard` | Admin only |
| `GET` | `/admin/users` | Admin only |
| `POST` | `/files/upload` | Authenticated users |

File uploads accept `.pdf`, `.jpg`, `.jpeg`, and `.png` files up to 5 MB. Uploaded files are renamed to UUID-based filenames before being written to `uploads/`.

## API Documentation

When the server is running, open:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI schema: `http://127.0.0.1:8000/openapi.json`

Use the **Authorize** button in Swagger UI and enter `Bearer <access-token>` to try protected routes.

## Run Tests

```bash
pytest
```

The tests require a configured database and seeded users. The current test suite expects a student account with username `sriharini` and password `password123` to exist before the protected-route tests run.

## Security Notes

- Store `SECRET_KEY` and database credentials outside source control.
- Use HTTPS in production so credentials and bearer tokens are encrypted in transit.
- Replace development credentials and avoid using them outside local development.
- Restrict database access to trusted hosts and use a least-privilege database user.
- Review upload storage, malware scanning, and retention requirements before production use.
