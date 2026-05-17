from jose import jwt
from datetime import datetime,timedelta

# SECRETE KEY
SECRETE_KEY="mysecretekey"

# ALGORITHMS
ALGORITHMS="HS256"

# TOKEN EXPIRY TIME:
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CREATE ACCESS TOKEN:
def create_access_token(data:dict):
    # data copy:
    to_encode=data.copy()

    # EXPIRY TIME:
    expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # ADD EXPIRY TO TOKEN
    to_encode.update({"exp":expire})

    # CREATE JWT TOKEN:
    encode_jwt=jwt.encode(
        to_encode,
        SECRETE_KEY,
        algorithm=ALGORITHMS
    )

    return encode_jwt