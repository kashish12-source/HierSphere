from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from models.job import Job
from models.users import User
from database.connections import SessionLocal
from schemas.job_schema import JobCreate
from auth.oauth2 import get_current_user,role_required,recruiter_only


router=APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

# create job:
@router.post("/jobs")
def create_job(job: JobCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # 1. Run the fixed security check
    recruiter_only(current_user)
    
    try:
        new_job = Job(
            title=job.title,
            company=job.company,
            location=job.location,
            salary=job.salary,
            description=job.description,
            recruiter_id=current_user.id  # Links the job to the logged-in user
        )
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        return {"message": "job has been created successfully", "job_id": new_job.id}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# get all jobs 
@router.get("/jobs")
def get_job(company:str=None,location:str=None,salary:int=None,title:str=None,db:Session=Depends(get_db)):
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

# update job:
@router.put("/jobs/{id}")
def update_job(id: int, update: JobCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # 1. Security Check
    recruiter_only(current_user)
    
    # 2. Find the job
    job_obj = db.query(Job).filter(Job.id == id).first()
    
    if not job_obj:
        raise HTTPException(status_code=404, detail="Job ID not found")

    # 3. Security: Ensure this recruiter owns this job
    if job_obj.recruiter_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only update your own jobs")

    # 4. Update fields
    job_obj.title = update.title
    job_obj.company = update.company
    job_obj.location = update.location
    job_obj.salary = update.salary
    job_obj.description = update.description
    
    db.commit()
    db.refresh(job_obj)
    return {"message": "Job has been updated successfully", "job": job_obj}

# delete job:
@router.delete("/jobs/{id}")
def delete_job(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # 1. Security Check
    recruiter_only(current_user)
    
    del_job = db.query(Job).filter(Job.id == id).first()
    
    if not del_job:
        raise HTTPException(status_code=404, detail="Job ID not found")

    # 2. Security: Ensure this recruiter owns this job
    if del_job.recruiter_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own jobs")

    db.delete(del_job)
    db.commit()
    return {"message": "job has been deleted successfully"}
