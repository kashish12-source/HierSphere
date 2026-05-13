from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from models.application import Application
from schemas.application_schema import ApplicationCreate,ApplicationStatusUpdate
from database.connections import SessionLocal
from auth.oauth2 import role_required

router=APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


# create application
@router.post("/applications")
def create_application(appli:ApplicationCreate ,db:Session=Depends(get_db),current_user: User = Depends(
        role_required("candidate")
    )):
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

@router.patch("/applications/{application_id}")
def update_only_one(application_id:int , application_status:ApplicationStatusUpdate ,db:Session=Depends(get_db)):
    application=db.query(Application).filter(Application.id==application_id).first()
    if not application:
        return "id not found "
    application.status=application_status.status
    db.commit()
    db.refresh(application)
    return "status has been updated successfully"