import json
from datetime import datetime
from uuid import uuid4
from fastapi.exceptions import HTTPException
import os
from sqlmodel import Session, SQLModel, create_engine, select

from backend.entities import (
    UserChatLinkInDB,
    UserInDB,
    UserCreate,
    UserUpdate,
    User,
    UserResponse,
    ChatInDB,
    ChatUpdate,
    MessageInDB,
    NewMessage,
    MessageResponse,
    Message
)

with open("backend/fake_db.json", "r") as f:
    DB = json.load(f)

class EntityNotFoundException(Exception):
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id

def get_all_users(session: Session) -> list[UserInDB]:
    """
    Retrieve all users from the database.

    :return: ordered list of users
    """
    return session.exec(select(UserInDB)).all()


def get_all_chats(session: Session) -> list[ChatInDB]:
    """
    Retrieve all chats from the database.

    :return: ordered list of chats
    """
    return session.exec(select(ChatInDB)).all()

def create_user(session: Session, user: UserCreate) -> UserInDB:
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
            created_at = datetime.now().isoformat(),
        )
        session.add(newUser)
        session.commit
        session.refresh(newUser)
        return newUser



def get_user_by_id(session: Session, user_id: int) -> UserInDB:
    """
    Retrieve a user from the database.

    :param user_id: id of the user to be retrieved
    :return: the retrieved user
    :raises EntityNotFoundException: if no such user id exists
    """
    user = session.get(UserInDB, user_id)
    if user:
        return user

    raise EntityNotFoundException(entity_name="User", entity_id=user_id)


def update_user(session: Session, user: UserInDB, user_update: UserUpdate):

    for attr, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, attr, value)

    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user









def get_chats_with_user(session: Session, user_id: int) -> list[ChatInDB]:
    #if user_id in DB["users"]:
    user = session.get(UserInDB, user_id)
    if user:
        return session.exec(select(ChatInDB).join(UserChatLinkInDB).where(UserChatLinkInDB.user_id == user_id)).all()
    raise EntityNotFoundException(entity_name="User", entity_id=user_id)
    

def get_messages_in_chat(session: Session, chat_id: int):
    chat = session.get(ChatInDB, chat_id)
    if chat:
        return session.exec(select(MessageInDB).where(MessageInDB.chat_id == chat_id)).all()
    raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)



def add_message(session: Session, user: UserInDB, chat_id: int, new_message: NewMessage):
    chat = get_chat_by_id(session, chat_id)
    messageInDB = MessageInDB(
            text = new_message.text,
            user_id=user.id,
            chat_id=chat.id,
            user = user,
            chat = chat,
            
        )
    session.add(messageInDB)
    session.commit()
    session.refresh(messageInDB)
    formattedUser = User(id=user.id, username=user.username, email=user.email, created_at=user.created_at)
    message = Message(
        id = messageInDB.id,
        text = new_message.text,
        chat_id=chat.id,
        user = formattedUser,
        created_at = messageInDB.created_at,
    )
    return MessageResponse(
        message=message
    )




def get_users_in_chat(session: Session, chat_id:int) -> list[UserInDB]:
   
    chat = session.get(ChatInDB, chat_id)
    if chat:
        return session.exec(select(UserInDB).join(UserChatLinkInDB).where(UserChatLinkInDB.chat_id == chat_id)).all()
    raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)


def get_chat_by_id(session: Session, chat_id: int) -> ChatInDB:
    """
    Retrieve a chat from the database.

    :param chat_id: id of the user to be retrieved
    :return: the retrieved user
    :raises EntityNotFoundException: if no such user id exists
    """
    chat = session.get(ChatInDB, chat_id)
    if chat:
        return chat

    raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)


def update_chat(session: Session, chat_id: int, chat_update: ChatUpdate ) -> ChatInDB:
    """
    Update an chat in the database.

    :param chat_id: id of the chat to be updated
    :param chat_update: attributes to be updated on the chat
    :return: the updated chat
    """

    chat = get_chat_by_id(session, chat_id)

    for attr, value in chat_update.model_dump(exclude_unset=True).items():
        setattr(chat, attr, value)

    
    session.add(chat)
    session.commit()
    session.refresh(chat)
    return chat

def delete_chat(session: Session, chat_id: int):
    """
    Delete an chat from the database.

    :param chat_id: the id of the chat to be deleted
    :raises EntityNotFoundException: if no such chat exists
    """

    chat = get_chat_by_id(session, chat_id)
    session.delete(chat)
    session.commit()



if os.environ.get("DB_LOCATION") == "RDS":
    username = os.environ.get("PG_USERNAME")
    password = os.environ.get("PG_PASSWORD")
    endpoint = os.environ.get("PG_ENDPOINT")
    port = os.environ.get("PG_PORT")
    db_url = f"postgresql://{username}:{password}@{endpoint}:{port}/{username}"
    echo = False
    connect_args = {}
else:
    db_url = "sqlite:///backend/pony_express.db"
    echo = True
    connect_args = {"check_same_thread": False}

engine = create_engine(
    db_url,
    echo=echo,
    connect_args=connect_args,
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session