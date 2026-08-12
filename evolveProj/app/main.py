# from unicodedata import category
from fastapi import FastAPI
from app.api import user, item , category, order, auth


app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(item.router, prefix="/items", tags=["Items"])
app.include_router(category.router, prefix="/categories", tags=["Categories"])
app.include_router(order.router, prefix= "/orders", tags=["Orders"])