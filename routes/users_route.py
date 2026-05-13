from fastapi import APIRouter ,Depends
from sqlalchemy.orm import Session 

from database.connections import SessionLocal
from schemas.users_schema import UserCreate
from models.users import User

from auth.hashing import hash_password

router=APIRouter()


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create user:

@router.post("/users")
def create_user(user:UserCreate,db:Session=Depends(get_db)):
    new_user=User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return "new_user"

# Get user:
@router.get("/users")
def get_users(db:Session=Depends(get_db)):
    return db.query(User).all()

