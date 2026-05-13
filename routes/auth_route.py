from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from database.connections import SessionLocal
from models.users import User
from schemas.users_schema import UserCreate,UserLogin
from auth.hashing import hash_password,verify_password
from auth.jwt_handler import create_access_token

router=APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup")
def sign_up(user:UserCreate,db:Session=Depends(get_db)):
    existing_user=db.query(User).filter(User.email==user.email).first()
    if existing_user:
        return "email already registered"
    
    # HASH PASSWORD:
    hashed_password=hash_password(user.password)

    # create user:
    new_user=User(
        username=user.username,
        email=user.email,
        password=hashed_password

    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return "user has been signed in successfully"


@router.post("/login")
def login(user:UserLogin,db:Session=Depends(get_db)):
    existing_user=db.query(User).filter(User.email==user.email).first()
    if not existing_user:
        return "enter valid id"
    password_correct=verify_password(
        user.password,
        existing_user.password
    )

    # generate token
    if not password_correct:
        return "enter valid password"
    access_token=create_access_token(data={"sub":existing_user.email})

    # return token

    return {
        "access_token":access_token,
        "token_type":"bearer"
    }
