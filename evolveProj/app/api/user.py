from typing import List
from fastapi import HTTPException, APIRouter, Depends, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
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


def check_if_db_exist(db: Session = Depends(get_db)):

    find_allUsers = users.select().where(users.c.id>=0).limit(1)
    search = db.execute(find_allUsers).first()
    if search is None :
            raise HTTPException(status_code=404,detail= "No users in Database")
    return 


router = APIRouter()

@router.get("",response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)):
    check_if_db_exist(db)
   
    fetch_all_users = users.select().where(users.c.deleted_at.is_(None)).with_only_columns(
    users.c.firstname,
    users.c.lastname,
    users.c.email,
    users.c.id)

    fetched = db.execute(fetch_all_users)
    list_of_users = fetched.mappings().all()
  
    return list_of_users
@router.get("/{user_id}",status_code=status.HTTP_200_OK)
def get_users_by_id(user_id: int,db: Session = Depends(get_db)):
    #check if Database exists
    check_if_db_exist(db)
    #find user
    #TODO: Make this it's own method in the user class, it's used multiple times
    query = users.select().where((users.c.id == user_id) & (users.c.deleted_at.is_(None)))
    user = db.execute(query).first()
    if user is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail =f"No user with the ID {user_id} exist")
    get_user = users.select().where((users.c.id == user_id) & (users.c.deleted_at.is_(None))).with_only_columns(
    users.c.firstname,
    users.c.lastname,
    users.c.email,
    users.c.id)
    get_from_db = db.execute(get_user)
    in_list = get_from_db.mappings().all()
    return in_list

@router.post("", response_model=CreateUser, status_code=status.HTTP_201_CREATED)
def add_user(makeUser: CreateUser, db: Session = Depends(get_db)):
    #check if the user already exists
    if (db.query(users).filter(users.c.email == makeUser.email).first()):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already in use")
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
@router.put("/{user_id}", status_code=status.HTTP_202_ACCEPTED)
def delete(id: int, db: Session = Depends(get_db)):
    #check if table exists
    check_if_db_exist(db)
    #check if user exists
    user = db.execute(users.select().where(users.c.id == id)).first()
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail =f"No user with the ID {id} exist")
    #check if user is already deleted
    is_deleted = db.execute(users.select().where((users.c.id == id ) & (users.c.deleted_at.is_(None)))).first()
    print(is_deleted)
    if is_deleted is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail =f"No user with the ID {id} was already deleted")
    #Soft deleting user

    delete_user =  users.update().where(users.c.id == id).values(deleted_at = func.current_timestamp())
    db.execute(delete_user)
    db.commit()


