from fastapi import FastAPI 
from routes.users_route import router as user_router
from routes.job_route import router as job_router 
from routes.application_route import router as app_route
from models.users import Base
from database.connections import engine

Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(user_router)
app.include_router(job_router)
app.include_router(app_route)
