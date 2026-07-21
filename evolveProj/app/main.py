from sqlalchemy.orm.session import Session
from fastapi import FastAPI, Depends
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from app.db.db_setup import engine
from typing import List
from app.api import user
from app.api.item import Items, CreateItem
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

# Users    
@app.get("/users/")
def get_allUsers(db: Session = Depends(get_db)):
    return user.get_all_users(db)
@app.post("/get_user_by_id/")
def get_user_by_id(user_id: int,db: Session = Depends(get_db)):
    return user.get_users_by_id(user_id, db)
@app.post("/createusers/")
def create_user(add_user: user.CreateUser, db: Session = Depends(get_db)):
 user_id = user.add_user(add_user, db)
 return {f"User with user id {user_id} has been added successfully!"}
 #TODO: Add autenticaion and role in order to only let certain users acces this
@app.put("/delete_user/")
def delete(user_id : int,db: Session = Depends(get_db)):
    user.delete(user_id,db)
    return {f"User with id {user_id} has been succesfully deleted"}

# Items
@app.get("/get_items_by_id/")
def get_items_by_id( item_id: int, db: Session = Depends(get_db)):
    item = Items.find_item(item_id,db)
    print_item= Items.print_items(item)
    return print_item

#TODO: Add autenticaion and role in order to only let certain users acces this
@app.post("/add_item/")
def create_item(add_item: CreateItem, db: Session = Depends(get_db)):
    new_item = Items.add_item(add_item, db)
    return {f"Item: {new_item} has been added successfully!"}

#Soft Delete Items
@app.put("/delete_items/")
def デリトリートーアイテム(id: int, db: Session= Depends(get_db)):
    Items.delete_item(id,db)
    return {f"Item with id: {id} has been deleted successfully"}

#Get all items
@app.get("/all_item/")
def get_all_items(db: Session = Depends(get_db)):
    return Items.get_all_items(db)
