from fastapi import FastAPI, Request

from app.database import Base, engine
from app.models.user import User

from app.routers.auth import router as auth_router
from app.routers.students import router as students_router
from app.routers.admin import router as admin_router
from app.routers.files import router as files_router

from app.logging_config import logger


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="Secure Student API",
    description="A secure student management backend using FastAPI, JWT and RBAC",
    version="1.0.0"
)


# Register routers
app.include_router(auth_router)
app.include_router(students_router)
app.include_router(admin_router)
app.include_router(files_router)


# Request and response logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):

    logger.info(
        f"Request: {request.method} {request.url.path}"
    )

    response = await call_next(request)

    logger.info(
        f"Response: {response.status_code} "
        f"for {request.method} {request.url.path}"
    )

    return response


# Home endpoint
@app.get("/")
def home():

    logger.info("Home endpoint accessed")

    return {
        "message": "Secure Student API is running"
    }