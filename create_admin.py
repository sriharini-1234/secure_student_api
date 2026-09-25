from app.database import SessionLocal
from app.models.user import User
from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


db = SessionLocal()

try:
    existing_admin = db.query(User).filter(
        User.username == "admin"
    ).first()

    if existing_admin:
        existing_admin.role = "admin"
        db.commit()
        print("Existing user updated to admin")

    else:
        admin = User(
            username="admin",
            email="admin@gmail.com",
            password=pwd_context.hash("admin123"),
            role="admin"
        )

        db.add(admin)
        db.commit()

        print("Admin user created")

finally:
    db.close()