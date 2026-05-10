from sqlalchemy import Column,Integer ,String
from database.connections import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"
    id =Column(Integer,primary_key=True,index=True)
    username= Column(String ,unique=True)
    email= Column(String, unique=True)
    password=Column(String)
    applications=relationship("Application",back_populates='user')
    
