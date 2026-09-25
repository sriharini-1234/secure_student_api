import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(
    Path(__file__).resolve().parent.parent / ".env"
)


SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set in .env")


ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30