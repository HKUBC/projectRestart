from ntpath import exists
from fastapi import HTTPException
from sqlalchemy import func
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


def check_if_db_exist(db: Session):

    find_allUsers = users.select().where(users.c.id>=0).limit(1)
    search = db.execute(find_allUsers).first()
    if search is None :
            raise HTTPException(status_code=404,detail= "No users in Database")
    return 


def get_all_users(db: Session):
    check_if_db_exist(db)
   
    fetch_all_users = users.select().where(users.c.deleted_at.is_(None)).with_only_columns(
    users.c.firstname,
    users.c.lastname,
    users.c.email,
    users.c.id)

    fetched = db.execute(fetch_all_users)
    list_of_users = fetched.mappings().all()
  
    return list_of_users

def get_users_by_id(user_id: int, db: Session):
    #check if Database exists
    check_if_db_exist(db)

    #find user
    #TODO: Make this it's own method in the user class, it's used multiple times
    user = db.execute(users.select().where(users.c.id == user_id)).first()
    #user = db.query(users).filter(users.c.id == user_id).first
    if user is None:
        raise HTTPException(status_code= 404, detail ="No user with the ID {user_id} exist")
    get_user = users.select().where(users.c.id == user_id and user.c.deleted_at.is_(None)).with_only_columns(
    users.c.firstname,
    users.c.lastname,
    users.c.email,
    users.c.id)
    get_from_db = db.execute(get_user)
    in_list = get_from_db.mappings().all()
    return in_list

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

def delete(id: int, db: Session):
    #check if table exists
    check_if_db_exist(db)
    #check if user exists
    user = db.execute(users.select().where(users.c.id == id)).first()
    if user is None:
        raise HTTPException(status_code= 404, detail ="No user with the ID {user_id} exist")
    #check if user is already deleted
    is_deleted = db.execute(users.select().where(users.c.id == id and user.c.deleted_at.is_(None)))
    if is_deleted is None:
        raise HTTPException(status_code= 404, detail ="No user with the ID {user_id} was already deleted")
    #Soft deleting user

    users.update().where(users.c.id == id).values(deleted_at = func.current_timestamp())


