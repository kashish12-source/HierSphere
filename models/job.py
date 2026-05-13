from sqlalchemy import Column,String ,Integer ,Float,ForeignKey
from database.connections import Base
from sqlalchemy.orm import relationship

class Job(Base):
    __tablename__="jobs"
    id = Column(Integer,primary_key=True,index=True)
    title  = Column(String )
    company =Column(String)
    location = Column(String)
    salary = Column(Integer)
    description = Column(String)
    applications=relationship("Application",back_populates='job')
    recrutier_id=Column( Integer,ForeignKey("user.id"))
    recrutier=relationship("User")
