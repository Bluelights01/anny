from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services import login 

router = APIRouter()
db_manager = login.MongoAuth()

class UserCredentials(BaseModel):
    username: str
    password: str

@router.post("/signup")
async def signup(user: UserCredentials):
    existing = await db_manager.get_user(user.username)
    if existing:
        return {"status":"failed","desc":"user_exist"}
    await db_manager.save_user(user.model_dump())
    return {"status": "success"}

@router.post("/login")
async def login(user: UserCredentials):
    db_user = await db_manager.get_user(user.username)
    if not db_user or db_user["password"] != user.password:
        return{"status":"failed"}
    return {"status": "success"}