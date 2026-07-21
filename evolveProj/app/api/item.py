from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.models.items.items_table import items 
from pydantic import BaseModel, ConfigDict
#from evolveProj.app.api.user import model_config

class CreateItem(BaseModel):
    price: float
    name: str
    category: str
    tag: str
class Item_response(BaseModel):
    id: int
    price: float
    name: str
    category: str
    tag: str
model_config = ConfigDict(from_attributes=True)

class Items:
   
    def search(id: int, db: Session):

        query = items.select().where((items.c.id == id) & (items.c.deleted_at.is_(None)))
        search = db.execute(query).first()
        if search is None:
            raise HTTPException(status_code=404, detail= "No items in Database")
        return
    def print_items(items):
        
        print_item = items.mappings().all()
        print("Inside print Items: ")
        return print_item 
        
    def table_exists (db: Session):
        find_any_item = items.select().where(items.c.id>=0).limit(1)
        search = db.execute(find_any_item).first()
        if search is None:
             raise HTTPException(status_code=404, detail= "No items in Database")
        return
        
    def find_item(id: int, db: Session):
        Items.table_exists(db) 
        Items.search(id, db)
        get_items = items.select().where((items.c.id == id) & (items.c.deleted_at.is_(None))).with_only_columns(
            items.c.id,
            items.c.price,
            items.c.name,
            items.c.category,
            items.c.tag
        )
        fetch_item = db.execute(get_items)
        return fetch_item
        #get_from_db = db.execute(get_items)
    def add_item(addItem: CreateItem, db: Session):
        Items.table_exists(db)
        # item_exists = items.select().where(items.c.id == addItem.id and items.c.name == addItem.name).first()
        # if not item_exists is None:
        #     raise HTTPException(status_code=409, detail=f"Item {addItem.name} has already been aded")
        if (db.query(items).filter((items.c.name ==addItem.name) & (items.c.category == addItem.category)& (items.c.tag == addItem.tag)).first()):
            raise HTTPException(status_code=409, detail=f"Item {addItem.name} has already exists")
        new_item = items.insert().values(
            price = addItem.price,
            name = addItem.name,
            category = addItem.category,
            tag = addItem.tag
        ).returning(items.c.name)
        adding = db.execute(new_item)
        db.commit()
        return adding.scalar()
    def delete_item(id: int, db: Session):
        Items.table_exists(db)
        Items.search(id, db)
        delete_item = items.update().where(items.c.id== id).values(deleted_at = func.current_timestamp())
        db.execute(delete_item)
        db.commit()
    def get_all_items(db: Session):
        Items.table_exists(db)
        query = items.select().where(items.c.deleted_at.is_(None)).with_only_columns(
            items.c.id,
            items.c.price,
            items.c.name,
            items.c.category,
            items.c.tag
        )
        get_all = db.execute(query)
        asList = get_all.mappings().all()
        return asList


