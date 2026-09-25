from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.models.user import User
from app.services.security import get_current_user


router = APIRouter(
    prefix="/files",
    tags=["Files"]
)


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png"
}

MAX_FILE_SIZE = 5 * 1024 * 1024


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="File type not allowed"
        )

    file_content = await file.read()

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 5 MB"
        )

    safe_filename = (
        f"{uuid4().hex}{extension}"
    )

    file_path = UPLOAD_DIR / safe_filename

    file_path.write_bytes(file_content)

    return {
        "message": "File uploaded successfully",
        "filename": safe_filename,
        "uploaded_by": current_user.username
    }