from fastapi import FastAPI
from pydantic import BaseModel


class User (BaseModel):
    user_ID: int
    name: str
    middle_name: str | None = None
    sir_name: str
    password: str
   

app = FastAPI()

@app.post(f"/creat_user/")
async def creat_user(user: User| None = None):
    if user.user_ID in User:
        return "Error: Cannot add the same user twice"
    return user


@app.get("/")
async def root():
    return {"message" : "Hello World"}


