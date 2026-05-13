from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError,jwt
from sqlalchemy.orm import Session

from database.connections import SessionLocal
from models.users import User
from auth.jwt_handler import SECRETE_KEY,ALGORITHM

# TOKEN URL
oauth2_scheme=OAuth2PasswordBearer(
    "token_url"="login"
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
    credential_exception=HTTPException(status_code=404,detail="could not validate")
    try:
        # DECODE TOKEN
        payload=jwt.decode(
            token,
            SECRETE_KEY,
            algorith=[ALGORITHM]
        )








