from fastapi import APIRouter, Depends

from app.models.user import User
from app.services.security import require_role


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/dashboard")
def admin_dashboard(
    current_user: User = Depends(
        require_role("admin")
    )
):
    return {
        "message": "Welcome to admin dashboard",
        "username": current_user.username,
        "role": current_user.role
    }


@router.get("/users")
def get_all_users(
    current_user: User = Depends(
        require_role("admin")
    )
):
    return {
        "message": "Admin can view all users",
        "username": current_user.username
    }