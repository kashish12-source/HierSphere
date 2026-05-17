from fastapi import FastAPI 
from routes.users_route import router as user_router
from routes.job_route import router as job_router 
from routes.auth_route import router as auth_route
from fastapi.middleware.cors import CORSMiddleware

from routes.application_route import router as app_route
from models.users import Base, User
from models.job import Job
from models.application import Application
from database.connections import engine
from auth.hashing import hash_password

from auth.jwt_handler import create_access_token

Base.metadata.create_all(bind=engine)

app=FastAPI()

# CROS configuration:
origins=[
 "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



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