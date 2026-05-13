from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError,jwt
from sqlalchemy.orm import Session

from database.connections import SessionLocal
from models.users import User
from auth.jwt_handler import SECRETE_KEY,ALGORITHMS

# TOKEN URL
oauth2_scheme=OAuth2PasswordBearer(
    tokenUrl="/login"
)

# DATABASE CONNECTION
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CURRENT USER FUNCTION:
def get_current_user(
    token:str=Depends(oauth2_scheme),
    db:Session=Depends(get_db)

):
    credential_exception=HTTPException(status_code=401,detail="could not validate")
    try:
        # DECODE TOKEN
        payload=jwt.decode(
            token,
            SECRETE_KEY,
            algorithms=[ALGORITHMS]
        )
        # GET EMAIL
        email=payload.get("sub")
        if email is None:
            raise credential_exception
    except JWTError :
        raise credential_exception

    # FIND USER:
    user=db.query(User).filter(User.email==email).first()
    if user is None:
        raise credential_exception
    
    return user

def recrutier_olny(current_user):
    if current_user.role!="recrutier":
        raise HTTPException(status_code=403,detail="only recrutiers allowed")
    return current_user

# role required:
def role_required(required_role:str):
    def role_checker(
        current_user:User=Depends(get_current_user)
    ):
        if current_user.role!=required_role:
            raise HTTPException(status_code=403 , detail="access denied")
        return current_user
    return role_checker





