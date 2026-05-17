from sqlalchemy import Integer, Column, String,ForeignKey
from database.connections import Base
from sqlalchemy.orm import relationship

class Application(Base):
    __tablename__="applications"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey('users.id'))
    job_id=Column(Integer,ForeignKey('jobs.id'))
    status=Column(String,default='pending')
    # RELATIONSHIPS:
    user=relationship("User", back_populates='applications')
    job=relationship("Job",back_populates='applications')
