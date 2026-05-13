from fastapi import FastAPI 
from routes.users_route import router as user_router
from routes.job_route import router as job_router 
from routes.auth_route import router as auth_route


from routes.application_route import router as app_route
from models.users import Base
from database.connections import engine
from auth.hashing import hash_password

from auth.jwt_handler import create_access_token

Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(user_router)
app.include_router(job_router)
app.include_router(app_route)
# print(hash_password("123456"))

# print(
#     create_access_token(
#         {"sub": "kashish@gmail.com"}
#     )
# )
app.include_router(auth_route)