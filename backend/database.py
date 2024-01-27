import json
from datetime import datetime
from uuid import uuid4
from fastapi.exceptions import HTTPException
from backend.entities import (
    UserInDB,
    UserCreate,
    ChatInDB,
    ChatUpdate,
    MsgInDB
)

with open("backend/fake_db.json", "r") as f:
    DB = json.load(f)

class EntityNotFoundException(Exception):
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id

def get_all_users() -> list[UserInDB]:
    """
    Retrieve all users from the database.

    :return: ordered list of users
    """

    return [UserInDB(**user_data) for user_data in DB["users"].values()]


def get_all_chats() -> list[ChatInDB]:
    """
    Retrieve all chats from the database.

    :return: ordered list of chats
    """

    return [ChatInDB(**chat_data) for chat_data in DB["chats"].values()]

def create_user(user: UserCreate) -> UserInDB:
    """
    Create a new user in the database.

    :param user_create: attributes of the user to be created
    :return: the newly created user
    """
    if user.id in DB["users"]:
        raise HTTPException(
            status_code = 422,
            detail={
                "type": "duplicate_entity",
                "entity_name": "User",
                "entity_id": user.id
            })
            
        
    else:
        newUser = UserInDB(
            id = user.id,
            created_at = datetime.now().isoformat()
        )
        DB["users"][user.id] = {"id": user.id, "created_at":newUser.created_at}
        return newUser



def get_user_by_id(user_id: str) -> UserInDB:
    """
    Retrieve a user from the database.

    :param user_id: id of the user to be retrieved
    :return: the retrieved user
    :raises EntityNotFoundException: if no such user id exists
    """

    if user_id in DB["users"]:
        return UserInDB(**DB["users"][user_id])

    raise EntityNotFoundException(entity_name="User", entity_id=user_id)




def get_chats_with_user(user_id: str) -> list[ChatInDB]:
    if user_id in DB["users"]:
        return [ChatInDB(**chat_data) for chat_data in DB["chats"].values() if user_id in chat_data.get("user_ids", [])]
    raise EntityNotFoundException(entity_name="User", entity_id=user_id)
    

def get_messages_in_chat(chat_id: str):
    if chat_id in DB["chats"]:
        chat_msgs = DB["chats"][chat_id].get("messages", [])
        return [MsgInDB(**message_data) for message_data in chat_msgs]
    raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

def get_users_in_chat(chat_id:str) -> list[UserInDB]:
    if chat_id in DB["chats"]:
        chat_user_ids = DB["chats"][chat_id].get("user_ids", [])
        return [get_user_by_id(user_id) for user_id in chat_user_ids]
    raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

def get_chat_by_id(chat_id: str) -> ChatInDB:
    """
    Retrieve a chat from the database.

    :param chat_id: id of the user to be retrieved
    :return: the retrieved user
    :raises EntityNotFoundException: if no such user id exists
    """

    if chat_id in DB["chats"]:
        return ChatInDB(**DB["chats"][chat_id])

    raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)


def update_chat(chat_id: str, chat_update: ChatUpdate) -> ChatInDB:
    """
    Update an chat in the database.

    :param chat_id: id of the chat to be updated
    :param chat_update: attributes to be updated on the chat
    :return: the updated chat
    """

    chat = get_chat_by_id(chat_id)
   
    for attr, value in chat_update.model_dump(exclude_none=True).items():
        setattr(chat, attr, value)
    return chat

def delete_chat(chat_id: str):
    """
    Delete an chat from the database.

    :param chat_id: the id of the chat to be deleted
    :raises EntityNotFoundException: if no such chat exists
    """

    chat = get_chat_by_id(chat_id)
    del DB["chats"][chat.id]
