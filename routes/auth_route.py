from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm
from auth.oauth2 import get_current_user
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
        password=hashed_password,
        role=user.role.strip().lower() if user.role else "candidate"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return "user has been signed in successfully"


# @router.post("/login")
# def login(user:UserLogin,db:Session=Depends(get_db)):
#     existing_user=db.query(User).filter(User.email==user.email).first()
#     if not existing_user:
#         return "enter valid id"
#     password_correct=verify_password(
#         user.password,
#         existing_user.password
#     )

#     # generate token
#     if not password_correct:
#         return "enter valid password"
#     access_token=create_access_token(data={"sub":existing_user.email})

#     # return token

#     return {
#         "access_token":access_token,
#         "token_type":"bearer"
#     }

@router.get("/profile")
def profile(current_user:User=Depends(get_current_user)):
    return {
        "id":current_user.id,
        "username":current_user.username,
        "email":current_user.email,
        "role":current_user.role
    }
@router.post("/login")
def login(
    user: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    # FIND USER
    existing_user = db.query(User).filter(
        User.email == user.username
    ).first()

    # CHECK EMAIL
    if not existing_user:

        raise HTTPException(
            status_code=404,
            detail="Invalid email"
        )

    # VERIFY PASSWORD
    password_correct = verify_password(
        user.password,
        existing_user.password
    )

    if not password_correct:

        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    # CREATE TOKEN
    access_token = create_access_token(
        data={
            "sub": existing_user.email,
            "user_id": existing_user.id,
            "role": existing_user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }