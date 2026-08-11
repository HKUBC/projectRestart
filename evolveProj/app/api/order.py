#FAST API imports
import random
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session

#table imports
from app.api.user import UserResponse, get_current_user
from app.db.models.user_information.user_table import users
from app.db.models.items.items_table import items
from app.db.models.orders.orders_table import orders
from app.db.models.mapping_tables.order_items import order_items
from app.db.db_setup import get_db

RAND_ID= int(random.random()*10000)

class createOrder(BaseModel):
    order_id: int
    user_id: int
class itemsOrderd(BaseModel):
    itemId: int
    quantity: int

class orderItems(BaseModel):
    id: int
    item_id: int
    quantity: int
    status: str

class userOrder(BaseModel):
    orderId: int
    orderedItems: list[itemsOrderd]

# def search(id: int, db: Session=Depends(get_db)):
#     item_orders.join(orders, item_orders.c.orders_id)   
#     pass
#todo: put this and all queries into repository folder
router = APIRouter()


#Creats an order with an ID associated with the user
@router.post("/create-order/{user_id}",status_code=status.HTTP_201_CREATED)
def create_order(user_id: Annotated[UserResponse, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    order_id= RAND_ID
    #get user ID
    find_userID_query = users.select().where(users.c.id == user_id)
    user = db.execute(find_userID_query).first()
    
    # if not user:
    #  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This user does not exist")
    create_order_query = orders.insert().values(
        order_id = order_id,
        user_id = user,
        status = "pending"
    ).returning(orders.c.id)
    result = db.execute(create_order_query).scalar()
    db.commit()
    return result
   
@router.post("/add-item/{orderId}/{itemId}",response_model=userOrder, status_code=status.HTTP_201_CREATED)
def add_item_to_order( orderId: int, itemId: int, quantity: int, authenticated_user:  Annotated[UserResponse, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    #verify that authenticated user is the same that created the order
    if not (orders.c.user_id == authenticated_user):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN)
    #get order ID
    find_orderID_query = orders.select().where(orders.c.id == orderId)
    # if not find_orderID_query:
    #     raise HTTPException(satus_code=status.HTTP_404_NOT_FOUND, detail="This order does not exist")
    order_id = db.execute(find_orderID_query).first()
    print(order_id)

    #Get item ID
    find_itemID_query = items.select().where(items.c.id == itemId)
    # if not find_itemID_query:
    #     raise HTTPException(satus_code=status.HTTP_404_NOT_FOUND, detail="This item does not exist")
    item_id = db.execute(find_itemID_query).first()

    #Creates order
    order_create_query = order_items.insert().values(
        order_id = order_id.id,
        item_id = item_id.id,
        quantity = quantity
    )
    db.execute(order_create_query)
    db.commit()
    added_items = order_items.select().where(order_items.c.id == orderId).first()
    db.execute()
    return added_items
#Add many items to 1 order
@router.post("/add-items/{orderId}", response_model=userOrder, status_code=status.HTTP_201_CREATED)
def add_items_to_order(orderId: int, order: list[itemsOrderd],authenticated_user:  Annotated[UserResponse, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    #Verify that order belongs to user

    #Get order ID
    find_orderID_query = orders.select().where(orders.c.id == orderId)
    find_orderId  = db.execute(find_orderID_query).first()
    if find_orderId is None:
        raise HTTPException(satus_code=status.HTTP_404_NOT_FOUND, detail="This order does not exist")
    order_id = db.execute(find_orderID_query).first()
    # inster_all_items_query = order_items.insert()
    
    values = [{
         "order_id": order_id.id,
         "item_id": item.itemId,
         "quantity": item.quantity

        }
        for item in order
      ]
    result = db.execute(order_items.insert(), values)
    db.commit()
    return result


@router.get("/user-id/{user_id}", response_model= list[orderItems], status_code=status.HTTP_302_FOUND)
def get_order_by_userID(user_id: Annotated[UserResponse, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    orders_by_user_query = orders.select().join(order_items, orders.c.id == order_items.c.order_id).where(orders.c.user_id == user_id).with_only_columns(
        orders.c.id,
        order_items.c.item_id,
        order_items.c.quantity,
        orders.c.status
    )
    get_orders = db.execute(orders_by_user_query).mappings().all()
    if not get_orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User {user_id} has not made any orders!")
    return  get_orders


@router.get("/order-id/{order_id}",response_model= list[orderItems], status_code=status.HTTP_302_FOUND)
def get_order_by_orderID(order_id: int, db: Annotated[Session, Depends(get_db)]):
    #
    orders_by_orderID_query = orders.select().join(order_items, orders.c.id == order_items.c.order_id).where(orders.c.id == order_id).with_only_columns(
        orders.c.id,
        order_items.c.item_id,
        order_items.c.quantity,
        orders.c.status
    )
    get_orders = db.execute(orders_by_orderID_query).mappings().all()
    if not get_orders:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  detail =f"Order with ID: {order_id} does not Exist!")
    return get_orders