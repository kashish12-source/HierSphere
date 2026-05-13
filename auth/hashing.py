from passlib.context import CryptContext

pwd_context=CryptContext(
    schemes=['bcrypt'],
    deprecated='auto'
)
# since int this pwd_context schemes =[bcrypt]because bcrypt is the hashing algo which is used by most of the high mncs like insta facebook etc
# deprecated auto means it can autotmatically handles the old hashing used for future compatibility


# HASH PASSWORD
def hash_password(password:str):
    return pwd_context.hash(password)

# verify password
def verify_password(plain_password:str,hashed_password:str):
    
    return pwd_context.verify( plain_password,hashed_password)
