from sqlalchemy.orm.session import Session
from fastapi import FastAPI, Depends
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from app.db.db_setup import engine
from typing import List
from app.api import user
# from app.api.user import UserResponse, CreateUser
# from app.db.models.user_information.user_table import users


#TODO: import api, db, and other services when done (user, etc)

app = FastAPI()


# Setup Database session
LocalSession = sessionmaker[Session](autocommit = False, autoflush = False, bind = engine )
Base = declarative_base()

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

get_db()

@app.get("/")
def sanity():
    return {"message": "Hello, I'm alive"}
    
@app.get("/users/")
def get_allUsers(db: Session = Depends(get_db)):
    return user.get_all_users(db)

@app.post("/createusers/")
def create_user(add_user: user.CreateUser, db: Session = Depends(get_db)):
 user_id = user.add_user(add_user, db)
 return {f"User with user id {user_id} has been added successfully!"}


