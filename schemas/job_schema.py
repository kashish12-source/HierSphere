from pydantic import BaseModel

class JobCreate(BaseModel):
    title:str
    company:str
    location:str
    salary:int
    description:str

class JobResponse(BaseModel):
    id:int
    title:str
    company:str
    location:str
    salary:int
    description:str
    
    class Config:
        from_attributes =True