# from unicodedata import category
from fastapi import FastAPI
from app.api import user, item , category


app = FastAPI()

# * Categories (using routers)
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(item.router, prefix="/items", tags=["Items"])
app.include_router(category.router, prefix="/categories", tags=["Categories"])