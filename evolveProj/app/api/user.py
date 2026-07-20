from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.user_information.user_table import users
from pydantic import BaseModel, ConfigDict


class CreateUser(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str

class UserResponse(BaseModel):
     firstname: str
     lastname: str
     email: str
     id: int
model_config = ConfigDict(from_attributes=True)

def get_all_users(db: Session):
    if not users:
        raise HTTPException(status_code=404,detail= "No users in Database")
    return db.query(users).all()

def add_user(makeUser: CreateUser, db: Session):
    #check if the user already exists
    

    if (db.query(users).filter(users.c.email == makeUser.email).first()):
        raise HTTPException(status_code=409 , detail="Email already in use")
    #Create and add user to the database
    newUser = users.insert().values(

        firstname = makeUser.firstname,
        lastname = makeUser.lastname,
        email = makeUser.email,
        password = makeUser.password
    ).returning(users.c.id)
    result = db.execute(newUser)
    db.commit()
    return result.scalar()
