# Secure Student API

A small student-management API built with FastAPI. It demonstrates account registration, login, protected routes, file uploads, and admin-only routes.

## Start Here

This project is a backend: it provides web addresses (API routes) that another program, Swagger UI, or PowerShell can call. It does not include a student-facing website.

Here are a few terms used in this README:

- **Route**: a URL and action, such as `GET /students/`.
- **Access token (JWT)**: a signed string returned after login. Send it with protected requests to prove who you are.
- **Role**: an account type. New accounts are `student`; some routes only allow `admin` accounts.
- **401 Unauthorized**: the request has no valid login token.
- **403 Forbidden**: the token is valid, but that account's role is not allowed to use the route.

## Features

- User registration and login with bcrypt password hashing
- JWT access tokens with a 30-minute lifetime
- Student and admin roles
- Protected student endpoints
- Admin-only dashboard and user endpoints
- Authenticated file uploads with extension and size validation
- Automatic request and response logging
- Interactive API documentation through Swagger UI and ReDoc

## Use Case

The basic workflow is:

1. A student creates an account. The API saves a password hash, not the plain-text password, and assigns the `student` role.
2. The student logs in. The API returns an access token.
3. The student includes that token when calling a protected route or uploading a file.
4. An administrator runs `python create_admin.py` to create or promote the `admin` account. Admin-only routes reject student accounts.

This is a learning/demo project, not a complete student-records system. The protected `GET /students/` route currently returns the logged-in user's username and role. It does not implement full create, read, update, and delete (CRUD) operations for student records.

## Tech Stack

- Python 3.12
- FastAPI and Uvicorn
- SQLAlchemy
- PostgreSQL
- Passlib with bcrypt for password hashing
- python-jose for JWT tokens
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

## Setup on Windows

You need Python 3.12 or later and PostgreSQL installed and running. In PostgreSQL, create an empty database named `secure_student_db` (for example, with pgAdmin). Keep the database name, username, and password for the next step.

Open PowerShell in this project folder, then create and activate a Python virtual environment:

	```powershell
	python -m venv venv
	.\venv\Scripts\Activate.ps1
	```

If PowerShell blocks activation, run this once in that terminal and then activate the environment again:

	```powershell
	Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
	.\venv\Scripts\Activate.ps1
	```

Install the libraries the project needs:

	```powershell
	pip install -r requirements.txt
	```

Create a file named `.env` in the project folder. Replace the example database username and password with your PostgreSQL credentials. `SECRET_KEY` is used to sign login tokens; keep it private.

	```dotenv
SECRET_KEY=replace-with-a-long-random-secret
DATABASE_URL=postgresql://postgres:your-password@localhost:5432/secure_student_db
	```

Start the API:

	```powershell
	uvicorn app.main:app --reload
	```

Leave this PowerShell window open while using the API. The API address is `http://127.0.0.1:8000`; interactive documentation is at `http://127.0.0.1:8000/docs`.

## Docker

Docker is an optional way to run the API in a container. Docker Desktop must be running, and PostgreSQL must still be available at the database address you provide. From PowerShell, build the image:

```powershell
docker build -t secure-student-api .
```

Then run it, replacing the database username and password:

```powershell
docker run --name secure-student-api -p 8000:8000 `
	-e SECRET_KEY=replace-with-a-long-random-secret `
	-e DATABASE_URL=postgresql://postgres:your-password@host.docker.internal:5432/secure_student_db `
  secure-student-api
```

The image creates `uploads/` and `logs/` inside the container. Files written there may be lost when the container is removed unless you configure persistent volumes.

## Create an Admin User

After the API environment and database are configured, open another PowerShell window in the project folder, activate the virtual environment, and run:

```powershell
 .\venv\Scripts\Activate.ps1
python create_admin.py
```

This creates the `admin` account or changes an existing account named `admin` to the admin role. The script contains a development password; inspect `create_admin.py` and change that password before using the project beyond local learning.

## Try the API

The commands below are for PowerShell. Keep the API running in its own terminal. First, create a student account; choose a username and email address that have not already been registered:

```powershell
$registerBody = @{
	username = "student1"
	email = "student1@example.com"
	password = "StrongPassword123!"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/auth/register" -ContentType "application/json" -Body $registerBody
```

Now log in with that account. The response includes an `access_token`:

```powershell
$loginBody = @{
	username = "student1"
	password = "StrongPassword123!"
} | ConvertTo-Json

$login = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/auth/login" -ContentType "application/json" -Body $loginBody
$token = $login.access_token
```

Use that token to call the protected student route:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/students/" -Headers @{ Authorization = "Bearer $token" }
```

The response should show the logged-in username and role. If you call this route without a token, `401 Unauthorized` is expected. If you use a student token on an admin-only route, `403 Forbidden` is expected. The login route accepts JSON, so use the commands above to obtain a token; `/docs` is useful for exploring the routes and request formats.

### Routes in this project

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

Swagger UI lets you inspect the routes and their request formats. Use the PowerShell login example above to call protected routes with a token.

## Run Tests

```powershell
pytest
```

The tests use the configured database. The protected-route tests expect a student account with username `sriharini` and password `password123`. If it does not exist, start the API and register it through `POST /auth/register` (use an unused email address), then run `pytest`. If a test fails, read the error output; a missing database or account can cause failures even when the API starts.

## Security Notes

- Store `SECRET_KEY` and database credentials outside source control.
- Use HTTPS in production so credentials and bearer tokens are encrypted in transit.
- Replace development credentials and avoid using them outside local development.
- Restrict database access to trusted hosts and use a least-privilege database user.
- Review upload storage, malware scanning, and retention requirements before production use.
