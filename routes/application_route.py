from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from models.application import Application
from schemas.application_schema import ApplicationCreate
from database.connections import SessionLocal

router=APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


# create application
@router.post("/applications")
def create_application(appli:ApplicationCreate ,db:Session=Depends(get_db)):
    new_appli=Application(
        user_id=appli.user_id,
        job_id=appli.job_id
    )
    db.add(new_appli)
    db.commit()
    db.refresh(new_appli)
    return "application added successfully"

#get application:
@router.get("/applicatioins")
def get_application(db:Session=Depends(get_db)):
    return db.query(Application).all()

