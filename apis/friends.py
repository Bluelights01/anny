from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from services import friends
from typing import Literal


router = APIRouter()
db_manager = friends.MongoFriends()

class UserSearch(BaseModel):
    query: str
    username:str
class CreateUser(BaseModel):
    username: str
class ReadArrayPayload(BaseModel):
    username: str
    field: Literal["sent", "requests", "friends"]

class ModifyArrayPayload(BaseModel):
    username: str
    field: Literal["sent", "requests", "friends"]
    target_username: str
class send_request_payload(BaseModel):
    source:str
    target:str
class accept_request_payload(BaseModel):
    source:str
    target:str
class reject_request_payload(BaseModel):
    source:str
    target:str

@router.post("/users")
async def search_users(payload: UserSearch):
    if not payload.query.strip():
        return {"status": "failed", "desc": "empty_query"}

    users = await db_manager.get_users_by_substring(payload.query)
    friends=await db_manager.read_array(payload.username,"friends")
    sent=await db_manager.read_array(payload.username,"sent")
    map={}
    for i in friends:
        map[i]=1
    for i in sent:
        map[i]=2
    dictlist={}
    for i in users:
        name=i["username"]
        if(name not in map):
            dictlist[name]="unknown"
        elif(map[name]==2):
            dictlist[name]="sent"
        else:
            dictlist[name]="friend"
            
    return {
        "status": "success",
        "users": dictlist
    }
@router.post("/users/create")
async def create_user(payload: CreateUser):
    username = payload.username.strip()

    if not username:
        return {"status": "failed", "desc": "empty_username"}

    await db_manager.create_user(username)

    return {
        "status": "success",
        "message": "user_friends_document_created"
    }
@router.post("/friends/read")
async def read_array(payload: ReadArrayPayload):
    username = payload.username.strip()

    if not username:
        return {"status": "failed", "desc": "empty_username"}

    data = await db_manager.read_array(username, payload.field)

    return {
        "status": "success",
        "field": payload.field,
        "data": data
    }
@router.post("/friends/add")
async def add_to_array(payload: ModifyArrayPayload):
    username = payload.username.strip()
    target = payload.target_username.strip()

    if not username or not target:
        return {"status": "failed", "desc": "empty_username"}

    if username == target:
        return {"status": "failed", "desc": "cannot_add_self"}

    await db_manager.add_to_array(username, payload.field, target)

    return {
        "status": "success",
        "message": f"{target} added to {payload.field}"
    }
@router.post("/friends/remove")
async def remove_from_array(payload: ModifyArrayPayload):
    username = payload.username.strip()
    target = payload.target_username.strip()

    if not username or not target:
        return {"status": "failed", "desc": "empty_username"}

    await db_manager.remove_from_array(username, payload.field, target)

    return {
        "status": "success",
        "message": f"{target} removed from {payload.field}"
    }
@router.post("/friends/send_request")
async def send_request(payload: send_request_payload):
    source = payload.source
    target = payload.target

    try:
        # Perform database updates
        await db_manager.add_to_array(target, "requests", source)
        await db_manager.add_to_array(source, "sent", target) # Changed from remove to add for a new request
        
        return {
            "status": "success",
            "message": f"Friend request sent from {source} to {target}"
        }
        
    except Exception as e:
        # Log the error here for debugging
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Could not process friend request"
        )
@router.post("/friends/reject_request")
async def reject_request(payload: reject_request_payload):
    source = payload.source
    target = payload.target

    try:
        # Perform database updates
        await db_manager.remove_from_array(source, "sent", target)
        await db_manager.remove_from_array(target, "requests", source)
        
        return {
            "status": "success",
            "message": f"Friend request rejected from {source} to {target}"
        }
        
    except Exception as e:
        # Log the error here for debugging
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Could not process reject request"
        )
@router.post("/friends/accept_request")
async def accept_request(payload: accept_request_payload):
    source = payload.source
    target = payload.target

    try:
        # Perform database updates
        await db_manager.add_to_array(target, "friends", source)
        await db_manager.add_to_array(source, "friends", target)

        await db_manager.remove_from_array(source,"sent",target)
        await db_manager.remove_from_array(target,"requests",source)
        await db_manager.remove_from_array(target,"sent",source)
        await db_manager.remove_from_array(source,"requests",target)
        
        return {
            "status": "success",
            "message": f"Friend request accepted from {source} to {target}"
        }
        
    except Exception as e:
        # Log the error here for debugging
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Could not process friend request"
        )
