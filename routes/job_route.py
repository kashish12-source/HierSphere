from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from models.job import Job
from database.connections import SessionLocal
from schemas.job_schema import JobCreate

router=APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

# create job:
@router.post("/jobs")
def create_job(job:JobCreate,db:Session=Depends(get_db)):
    new_job=Job(
        title=job.title,
        company=job.company,
        location=job.location,
        salary=job.salary,
        description=job.description
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return "job has been created successfully"

# get all jobs 
@router.get("/jobs")
def get_job(db:Session=Depends(get_db)):
    return db.query(Job).all()

# update job:
@router.put("/jobs/{id}")
def update_job(id: int, update: JobCreate, db: Session = Depends(get_db)):
    job_obj = db.query(Job).filter(Job.id == id).first()
    if job_obj:
        job_obj.title = update.title
        job_obj.company = update.company
        job_obj.location = update.location
        job_obj.salary = update.salary
        job_obj.description = update.description
        db.commit()
        db.refresh(job_obj)
        return {"message": "Job has been updated successfully", "job": job_obj}
    else:
        return {"error": "id not found, please enter a valid id"}

        return "id not found please enter the valid id "

# delete job:
@router.delete("/jobs")
def delete_job(id:int ,db:Session=Depends(get_db)):
    del_job=db.query(Job).filter(Job.id==id).first()
    if del_job:
        db.delete(del_job)
        db.commit()
        return "job has been deleted successfully"
    else:
        return "please enter the valid id no."

# get data with filter :
@router.get("/jobss")
def filtered_data(company:str=None,location:str=None,salary:int=None,title:str=None,db:Session=Depends(get_db)):
    query=db.query(Job)
    # filter by company
    if company:
        query=query.filter(Job.company==company)
    
    # filter by location:
    if location:
        query=query.filter(Job.location==location)
    
    # filter by salary:
    if salary:
        query=query.filter(Job.salary>=salary)
    
    # filter by title:
    if title:
        query=query.filter(Job.title==title)

    # execute query:
    jobs=query.all()
    return jobs

