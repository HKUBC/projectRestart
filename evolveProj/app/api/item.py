from typing import List
from fastapi import HTTPException, APIRouter, Depends, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
from app.db.models.items.items_table import items 
from app.db.models.items.categories_table import categories
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



# class Items:

#     # #Helper to find items
#     # def search(id: int, db: Session=Depends(get_db)):

#     #     query = items.select().where((items.c.id == id) & (items.c.deleted_at.is_(None)))
#     #     search = db.execute(query).first()
#     #     if search is None:
#     #         raise HTTPException(status_code=404, detail= "No items in Database")
#     #     return
#     # # Helps printing items
#     # def print_items(items):
        
#     #     print_item = items.mappings().all()
#     #     return print_item 
#     # #checks if the table exists
#     # # # ! Code might be redundant with other checks, further testing required    
#     # # def table_exists (db: Session=Depends(get_db)):
#     # #     find_any_item = items.select().where(items.c.id>=0).limit(1)
#     # #     search = db.execute(find_any_item).first()
#     # #     if search is None:
#     # #          raise HTTPException(status_code=404, detail= "No items in Database")
#     # #     return
#     # # Search for an Item   
#     # @router.get("",response_model=Item_response,stats_code=status.HTTP_200_OK)
#     # def find_item(id: int, db: Session=Depends(get_db)):
#     #     Items.table_exists(db) 
#     #     Items.search(id, db)
#     #     #Joins the 'items' and 'categories' tables in order to return a more comprehensive item to the user
#     #     get_items_join = items.select().join(categories, items.c.category_id == categories.c.id).where(
#     #         (items.c.id == id) & (items.c.deleted_at.is_(None))
#     #         ).with_only_columns(
#     #         items.c.id,
#     #         items.c.price,
#     #         items.c.name,
#     #         categories.c.name,
#     #         items.c.tag
#     #     )

#     #     # #! Method without join, here to test if this breaks, delete after 
#     #     # get_items = items.select().where((items.c.id == id) & (items.c.deleted_at.is_(None))).with_only_columns(
#     #     #     items.c.id,
#     #     #     items.c.price,
#     #     #     items.c.name,
#     #     #     items.c.category,
#     #     #     items.c.tag
#     #     # )

#     #     fetch_item = db.execute(get_items_join)



#     #    # fetch_item = db.execute(get_items)

#     #     return fetch_item
#     #     #get_from_db = db.execute(get_items)

#     # # Create new Item 
#     # @router.post("",response_model=CreateItem, status_code=status.HTTP_200_OK)   
#     # def add_item(addItem: CreateItem, db: Session=Depends(get_db)):

#     #      # Get entered catgory, find the category ID and return it
#     #     #TODO: Find code to change string to lowercase, or match while ignoring cases
         
#     #     id_query = categories.select().where((categories.c.category == addItem.category) & (categories.c.deleted_at.is_(None))).with_only_columns(categories.c.id)
#     #     cat_id = db.execute(id_query).scalar()
#     #     items_query_filter = (items.c.name ==addItem.name) & (items.c.category_id == cat_id)& (items.c.tag == addItem.tag)
#     #     if (db.query(items).filter(items_query_filter).first()):
#     #         raise HTTPException(status_code=409, detail=f"Item {addItem.name} already exists")
       
        
#     #     # Insert new Item in db
#     #     new_item = items.insert().values(
#     #         price = addItem.price,
#     #         name = addItem.name,
#     #         category_id = cat_id,
#     #         tag = addItem.tag
#     #     ).returning(items.c.name)
#     #     adding = db.execute(new_item)
#     #     db.commit()
#     #     return adding.scalar()

#     # #Delete Items 
#     # @router.put("/{id}",status_code=status.HTTP_200_OK)
#     # def delete_item(id: int, db: Session=Depends(get_db)):
#     #     Items.table_exists(db)
#     #     Items.search(id, db)
#     #     delete_item = items.update().where(items.c.id== id).values(deleted_at = func.current_timestamp())
#     #     db.execute(delete_item)
#     #     db.commit()
#     # def get_all_items(db: Session=Depends(get_db)):
#     #     Items.table_exists(db)
#     #     query = items.select().where(items.c.deleted_at.is_(None)).with_only_columns(
#     #         items.c.id,
#     #         items.c.price,
#     #         items.c.name,
#     #         items.c.category_id,
#     #         items.c.tag
#     #     )

#     #     get_all = db.execute(query)
#     #     asList = get_all.mappings().all()
#     #     return asList

 #Helper to find items
def search(id: int, db: Session=Depends(get_db)):

        query = items.select().where((items.c.id == id) & (items.c.deleted_at.is_(None)))
        search = db.execute(query).first()
        if search is None:
            raise HTTPException(status_code=404, detail= "No items in Database")
        return
    # Helps printing items
def print_items(items):
        
        print_item = items.mappings().all()
        return print_item 
    #checks if the table exists
    # ! Code might be redundant with other checks, further testing required    
def table_exists (db: Session=Depends(get_db)):
        find_any_item = items.select().where(items.c.id>=0).limit(1)
        search = db.execute(find_any_item).first()
        if search is None:
             raise HTTPException(status_code=404, detail= "No items in Database")
        return
    # Search for an Item  
router = APIRouter()

@router.get("",response_model=Item_response,status_code=status.HTTP_200_OK)
def find_item(id: int, db: Session=Depends(get_db)):
    table_exists(db) 
    search(id, db)
        #Joins the 'items' and 'categories' tables in order to return a more comprehensive item to the user
    get_items_join = items.select().join(categories, items.c.category_id == categories.c.id).where(
        (items.c.id == id) & (items.c.deleted_at.is_(None))
        ).with_only_columns(
        items.c.id,
        items.c.price,
        items.c.name,
        categories.c.name,
        items.c.tag
        )

        # #! Method without join, here to test if this breaks, delete after 
        # get_items = items.select().where((items.c.id == id) & (items.c.deleted_at.is_(None))).with_only_columns(
        #     items.c.id,
        #     items.c.price,
        #     items.c.name,
        #     items.c.category,
        #     items.c.tag
        # )

    fetch_item = db.execute(get_items_join)



       # fetch_item = db.execute(get_items)

    return fetch_item
        #get_from_db = db.execute(get_items)

    # Create new Item 
@router.post("",response_model=CreateItem, status_code=status.HTTP_200_OK)   
def add_item(addItem: CreateItem, db: Session=Depends(get_db)):

         # Get entered catgory, find the category ID and return it
        #TODO: Find code to change string to lowercase, or match while ignoring cases
         
        id_query = categories.select().where((categories.c.category == addItem.category) & (categories.c.deleted_at.is_(None))).with_only_columns(categories.c.id)
        cat_id = db.execute(id_query).scalar()
        items_query_filter = (items.c.name ==addItem.name) & (items.c.category_id == cat_id)& (items.c.tag == addItem.tag)
        if (db.query(items).filter(items_query_filter).first()):
            raise HTTPException(status_code=409, detail=f"Item {addItem.name} already exists")
       
        
        # Insert new Item in db
        new_item = items.insert().values(
            price = addItem.price,
            name = addItem.name,
            category_id = cat_id,
            tag = addItem.tag
        ).returning(items.c.name)
        adding = db.execute(new_item)
        db.commit()
        return adding.scalar()

    #Delete Items 
@router.put("/{id}",status_code=status.HTTP_200_OK)
def delete_item(id: int, db: Session=Depends(get_db)):
    table_exists(db)
    search(id, db)
    delete_item = items.update().where(items.c.id== id).values(deleted_at = func.current_timestamp())
    db.execute(delete_item)
    db.commit()
def get_all_items(db: Session=Depends(get_db)):
    table_exists(db)
    query = items.select().where(items.c.deleted_at.is_(None)).with_only_columns(
            items.c.id,
            items.c.price,
            items.c.name,
            items.c.category_id,
            items.c.tag
        )

    get_all = db.execute(query)
    asList = get_all.mappings().all()
    return asList
