from fastapi import APIRouter, Depends
from datetime import date
from typing import Literal
from fastapi.exceptions import HTTPException
from backend.auth import get_current_user
from backend.entities import (
    User,
    UserInDB,
    ChatInDB,
    ChatCollection,
    ChatResponse,
    ChatUpdate,
    Chat,
    MsgCollection,
    MessageResponse,
    NewMessage,
    UserCollection,
)
from backend import database as db
from sqlmodel import Session


chats_router = APIRouter(prefix="/chats", tags=["Chats"])

@chats_router.post(
    "/{chat_id}/messages",
    response_model=MessageResponse,
    description="Creates a new message for chat with the given chat id.",
    status_code=201
)
def post_msg(new_message: NewMessage, chat_id= int, user: UserInDB = Depends(get_current_user),  session: Session = Depends(db.get_session)):
    
    return db.add_message(session, user, chat_id, new_message)



@chats_router.get("", 
                  response_model=ChatCollection,
                  description="Get all chats.",)
def get_chats(session: Session = Depends(db.get_session)):
    chatsInDB = db.get_all_chats(session)
    chats_response = []
    for chat in chatsInDB:
        userInDB = db.get_user_by_id(session,chat.owner.id)
        userResponse = User(id=userInDB.id, username=userInDB.username, email=userInDB.email, created_at=userInDB.created_at)
        chat_response = Chat(id=chat.id, name=chat.name, owner=userResponse, created_at=chat.created_at)
        chats_response.append(chat_response)
    sort_key = lambda chat: chat.name
    return ChatCollection(
        meta={"count": len(chats_response)},
        chats=sorted(chats_response, key=sort_key),
    )

@chats_router.get(
    "/{chat_id}",
    response_model=ChatResponse,
    description="Get a chat with the given chat id.",
)
def get_chat(chat_id: int, session: Session = Depends(db.get_session)):
    """Get a chat for a given id."""
    
    return ChatResponse(chat=db.get_chat_by_id(session, chat_id))

@chats_router.put("/{chat_id}", 
                  response_model=ChatResponse,
                  description="Updates a chat with the given chat id.",)
def update_chat(chat_id: int, chat_update: ChatUpdate, session: Session = Depends(db.get_session)):
    """Update an chat for a given id."""
    chatInDB = db.update_chat(session, chat_id, chat_update)
    userInDB = db.get_user_by_id(session,chatInDB.owner.id)
    userResponse = User(id=userInDB.id, username=userInDB.username, email=userInDB.email, created_at=userInDB.created_at)
    chat_response = Chat(id=chatInDB.id, name=chatInDB.name, owner=userResponse, created_at=chatInDB.created_at)
    return ChatResponse(
        chat=chat_response
    )

@chats_router.get(
    "/{chat_id}/messages",
    response_model=MsgCollection,
    description="Get messages for chat with given chat id.",
)
def get_msgs(chat_id: int, session: Session = Depends(db.get_session)):
    messagesInDB = db.get_messages_in_chat(session, chat_id)

    messages = []
    for message in messagesInDB:
        userInDB = message.user
        messageUser = User(id=userInDB.id, username=userInDB.username, email=userInDB.email, created_at=userInDB.created_at)
        message = MessageResponse(id= message.id, text= message.text, chat_id= message.chat_id, user= messageUser, created_at=message.created_at)
        messages.append(message)
    sort_key = lambda msg: msg.created_at
    return MsgCollection(
        meta={"count": len(messages)},
        messages=sorted(messages, key=sort_key),
    )

@chats_router.get(
    "/{chat_id}/users",
    response_model=UserCollection,
    description="Get users for chat with given chat id.",
)
def get_users(chat_id: int, session: Session = Depends(db.get_session)):
    usersInDB = db.get_users_in_chat(session, chat_id)
    users = [User(id=user.id, username=user.username, email=user.email, created_at=user.created_at)
             for user in usersInDB]
    sort_key = lambda user: user.id
    return UserCollection(
        meta={"count": len(users)},
        users=sorted(users, key=sort_key),
    )

    

    



