from fastapi import APIRouter, Depends

from app.models.user import User
from app.services.security import get_current_user


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.get("/")
def get_students(
    current_user: User = Depends(get_current_user)
):
    return {
        "message": "You can access the student API",
        "username": current_user.username,
        "role": current_user.role
    }