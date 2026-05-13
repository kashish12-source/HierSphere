from pydantic import BaseModel
# in fastapi schemas are used to define what datashould api accept and what data should api return 

class UserCreate(BaseModel):
    username:str 
    email:str
    password:str
    role:str="candidate"
class UserLogin(BaseModel):
    email:str
    password:str

class UserResponse(BaseModel):
    id:int 
    username:str
    email:str

    class Config:
        from_attributes=True


# the main diffrenece between the UserCreate and UserResponse is that when the User is created the ID is not known by the user before
# creation as it is created automatically and when the api response to the user it will send the ID 

# thats why the UserResponse contain the id and user create does not 

# why do we use the class config :
# we use the class config because when the api sends the response it will send the response in the form of sqlalchemy object so the 
# to extract value from the object and convert the data into the json response we use the class config which contain the orm_mode=True;
