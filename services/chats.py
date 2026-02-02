
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId

load_dotenv()

client = MongoClient(os.getenv("RAG_MONGO_URI"))
db = client["rag_db"]
collection = db["conversations"]

def create_new_chat(username, title, desc, blue_prompt, red_prompt):
    """
    Creates a new chat document in MongoDB.
    
    Args:
        username (str): Name of the user creating the chat
        title (str): Title of the chat
        desc (str): Description of the chat
        blue_prompt (str): Blue prompt content
        red_prompt (str): Red prompt content
    
    Returns:
        str: ID of the newly created chat
    """
    chat_doc = {
        "username": username,
        "title": title,
        "desc": desc,
        "blue_prompt": blue_prompt,
        "red_prompt": red_prompt,
        "messages": []  # empty for now
    }

    result = collection.insert_one(chat_doc)
    print(f"New chat created with ID: {result.inserted_id}")
    return str(result.inserted_id)


def add_message(chat_id, msg_type, message_text, embedding):
    """
    Adds a message to the messages array of a chat document.

    Args:
        chat_id (str): The ID of the chat document
        msg_type (str): Type of the message (e.g., "user", "bot", "system")
        message_text (str): The content of the message
        embedding (list[float]): The embedding vector for the message

    Returns:
        bool: True if message was added successfully, False otherwise
    """
    try:
        # Convert string ID to ObjectId
        obj_id = ObjectId(chat_id)

        # Create the message object
        message_doc = {
            "type": msg_type,
            "message_text": message_text,
            "embedding": embedding
        }

        # Append the message to the messages array
        result = collection.update_one(
            {"_id": obj_id},
            {"$push": {"messages": message_doc}}
        )

        if result.modified_count == 1:
            print(f"Message added to chat {chat_id}")
            return True
        else:
            print(f"No chat found with ID {chat_id}")
            return False

    except Exception as e:
        print(f"Error adding message: {e}")
        return False

def read_chat(chat_id):
    """
    Retrieves the messages array of a chat document by ID.

    Args:
        chat_id (str): The ID of the chat document

    Returns:
        list: List of messages, or None if chat not found
    """
    try:
        obj_id = ObjectId(chat_id)
        chat_doc = collection.find_one({"_id": obj_id}, {"messages": 1})

        if chat_doc:
            return chat_doc.get("messages", [])
        else:
            print(f"No chat found with ID {chat_id}")
            return None

    except Exception as e:
        print(f"Error reading chat: {e}")
        return None

def get_latest_message(chat_id):
    """
    Fetches the latest message from the messages array of a chat document.

    Args:
        chat_id (str): The ID of the chat document

    Returns:
        dict: Latest message object, or None if chat not found or no messages
    """
    try:
        obj_id = ObjectId(chat_id)

        # Fetch only the last message using projection and slice
        chat_doc = collection.find_one(
            {"_id": obj_id},
            {"messages": {"$slice": -1}}  # gets only the last element
        )

        if chat_doc and "messages" in chat_doc and len(chat_doc["messages"]) > 0:
            return chat_doc["messages"][0]
        else:
            print(f"No messages found for chat {chat_id}")
            return None

    except Exception as e:
        print(f"Error fetching latest message: {e}")
        return None
    
def list_messages():
    """
    Fetches a list of all chat documents with their IDs and titles.

    Returns:
        list of dict: Each dict contains 'id' and 'title'
    """
    try:
        # Find all chats, only return _id and title
        chats = collection.find({}, {"_id": 1, "title": 1})
        chat_list = [{"id": str(chat["_id"]), "title": chat["title"]} for chat in chats]
        return chat_list

    except Exception as e:
        print(f"Error listing messages: {e}")
        return []
