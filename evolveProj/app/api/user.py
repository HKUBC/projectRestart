from datetime import timedelta
from typing import Annotated, List
from fastapi import HTTPException, APIRouter, Depends, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
from app.db.models.user_information.user_table import users
from pydantic import BaseModel, ConfigDict
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from app.api.auth import hash_password, create_access_token,verify_access_token, verify_password, oauth2_scheme
from app.api.config import settings


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated= 'auto')

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


def check_if_db_exist(db: Annotated[Session, Depends(get_db)]):

    find_allUsers = users.select().where(users.c.id>=0).limit(1)
    search = db.execute(find_allUsers).first()
    if search is None :
            raise HTTPException(status_code=404,detail= "No users in Database")
    return 
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]):
    #Get currently authenticated user
 user_id = verify_access_token(token)
 if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Invalid or expired token")
 try:
        user_id_int = int(user_id)
 except(TypeError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Invalid or expired token")
 get_current_user_query = users.select().where(users.c.id == user_id_int)
 result = db.execute(get_current_user_query)
 user = result.scalars().first()
 if not user:
    raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "User not found")

 return user

router = APIRouter()

@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(makeUser: CreateUser, db: Annotated[Session, Depends(get_db)]):
    #check if the user already exists
    if (db.query(users).filter(users.c.email == makeUser.email).first()):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already in use")
    
    #Hash user password
    hashed_password = hash_password(makeUser.password)
    #Create and add user to the database

    newUser = users.insert().values(

        firstname = makeUser.firstname,
        lastname = makeUser.lastname,
        email = makeUser.email,
        password = hashed_password
    ).returning(users.c.id)
    result = db.execute(newUser)
    db.commit()
    return result.scalar()

@router.post("/token")
def log_in_for_access_token( form_data: Annotated[OAuth2PasswordRequestForm, Depends()] ,db: Annotated[Session, Depends(get_db)]):

 find_user_query = users.select().where(func.lower(users.c.email) == form_data.username.lower())
 user = db.execute(find_user_query).first()
 hashed_password = user._mapping['password']
 #verify user info
 if user is None or not verify_password(form_data.password, hashed_password):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Wrong email or password")



 userID = user._mapping["id"]

 access_token_expires = timedelta(minutes = settings.access_token_expire)



 access_token = create_access_token(data = {"sub": str(userID)},
 expires_delta= access_token_expires
 )

 return {
    "access_token": access_token,
    "token_type": "bearer"
         }


@router.get("/me", response_model=UserResponse)
def me(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    return current_user


@router.get("",response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def get_users(db: Annotated[Session, Depends(get_db)]):
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
def get_user(user_id: Annotated[UserResponse, Depends(get_current_user)],db: Annotated[Session, Depends(get_db)]):
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

@router.patch("/change-password")
def change_password(user_id: Annotated[UserResponse, Depends(get_current_user)], password: str, new_password: str, new_password2: str, db: Annotated[Session, Depends(get_db)]):
    #Verify old password
 find_user_query = users.select().where(users.c.id == user_id)
 user = db.execute(find_user_query).first()
 #Only for testing, should not be needed later
 if user is None:
    raise HTTPException()
 hashed_password = user._mapping['password']
 if not bcrypt_context.verify(password, hashed_password):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "password is incorrect")
 if not (new_password == new_password2):
    raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "two different passwords entered")
 #hash new password
 new_hashed_password = bcrypt_context.hash(new_password)
 update_password_query = users.update().where(users.c.id == user_id).values(password = new_hashed_password)
 db.execute(update_password_query)
 db.commit()


@router.delete("/{user_id}", status_code=status.HTTP_202_ACCEPTED)
def delete(id:Annotated[UserResponse, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
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

    delete_user_query =  users.update().where(users.c.id == id).values(deleted_at = func.current_timestamp())
    db.execute(delete_user_query)
    db.commit()


