import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

class MongoAuth:
    def __init__(self):
        # Establish connection to MongoDB
        self.client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
        self.db = self.client['creds']
        self.collection = self.db.users

    # --- PUSH DATA (Signup) ---
    async def save_user(self, user_data: dict):
        """
        user_data should be: {"username": "...", "password": "..."}
        """
        result = await self.collection.insert_one(user_data)
        return str(result.inserted_id)

    # --- FETCH DATA (Login) ---
    async def get_user(self, username: str):
        """
        Retrieves the user document by username
        """
        user = await self.collection.find_one({"username": username})
        if user:
            # MongoDB adds an _id field; we convert it to string for JSON safety
            user["_id"] = str(user["_id"])
            return user
        return None
