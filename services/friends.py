import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import re

load_dotenv()

class MongoFriends:
    def __init__(self):
        self.client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
        self.db = self.client['friends']
        self.collection = self.db.requests

    # ---------- helper ----------
    async def _ensure_user_exists(self, username: str):
        await self.create_user(username)

    # ---------- search ----------
    async def get_users_by_substring(self, substring: str):
        query = {
            "username": {
                "$regex": re.escape(substring),
                "$options": "i"
            }
        }
        db = self.client['creds']
        collection = db.users

        users = []
        cursor = collection.find(query, {"_id": 0, "password": 0})

        async for user in cursor:
            users.append(user)

        return users

    # ---------- add ----------
    async def add_to_array(self, username: str, field: str, target_username: str):
        if field not in ("sent", "requests", "friends"):
            raise ValueError("Invalid field name")

        await self._ensure_user_exists(username)

        await self.collection.update_one(
            {"username": username},
            {"$addToSet": {field: target_username}}
        )

    # ---------- remove ----------
    async def remove_from_array(self, username: str, field: str, target_username: str):
        if field not in ("sent", "requests", "friends"):
            raise ValueError("Invalid field name")

        await self._ensure_user_exists(username)

        await self.collection.update_one(
            {"username": username},
            {"$pull": {field: target_username}}
        )

    # ---------- read ----------
    async def read_array(self, username: str, field: str):
        if field not in ("sent", "requests", "friends"):
            raise ValueError("Invalid field name")

        await self._ensure_user_exists(username)

        doc = await self.collection.find_one(
            {"username": username},
            {field: 1, "_id": 0}
        )

        return doc.get(field, [])

    # ---------- create ----------
    async def create_user(self, username: str):
        await self.collection.update_one(
            {"username": username},
            {
                "$setOnInsert": {
                    "username": username,
                    "sent": [],
                    "requests": [],
                    "friends": []
                }
            },
            upsert=True
        )
