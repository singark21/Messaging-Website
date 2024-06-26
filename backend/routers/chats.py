from fastapi import APIRouter, Depends, Query
from datetime import date
from typing import List, Literal,Optional
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
    Message,
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
    chatInDB = db.get_chat_by_id(session, chat_id)

    if user not in chatInDB.users:
        raise HTTPException(
            status_code = 403,
            detail={
                "error": "no_permission",
                "error_description": "requires permission to view chat"
            })
    return db.add_message(session, user, chat_id, new_message)



@chats_router.get("", 
                  response_model=ChatCollection,
                  description="Get all chats.",)
def get_chats(session: Session = Depends(db.get_session), user: UserInDB = Depends(get_current_user)
):
    chatsInDB = db.get_chats_with_user(session,user.id)
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
    description="Retrieve a chat by id",
    #response_model=ChatResponse
)
def get_chat(
    chat_id: int,
    include: List[str] = Query([], description="List of keys to include in the response"),
    session: Session = Depends(db.get_session),
    user: UserInDB = Depends(get_current_user),
):
    """
    Returns a chat using the provided chat ID.
    """
    chatInDB = db.get_chat_by_id(session, chat_id)

    if user not in chatInDB.users:
        raise HTTPException(
            status_code = 403,
            detail={
                "error": "no_permission",
                "error_description": "requires permission to view chat"
            })

    userInDB = db.get_user_by_id(session,chatInDB.owner.id)
    userResponse = User(id=userInDB.id, username=userInDB.username, email=userInDB.email, created_at=userInDB.created_at)

    chat = Chat(id=chatInDB.id, name=chatInDB.name, owner=userResponse, created_at=chatInDB.created_at)
    messages = db.get_messages_in_chat(session, chat_id)
    meta = {"message_count":len(messages), "user_count": len(chatInDB.users)}

    response_data = {"meta": meta, "chat": chat}

    if "messages" in include:
        updatedMessages = [Message(id=message.id, text=message.text, chat_id=message.chat_id, user=message.user,created_at = message.created_at)
             for message in messages]
        response_data["messages"] = updatedMessages

    if "users" in include:
        users = db.get_users_in_chat(session, chat_id)
        updatedUsers = [User(id=user.id, username=user.username, email=user.email, created_at=user.created_at)
             for user in users]
        response_data["users"] = updatedUsers

    return response_data




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
def get_msgs(chat_id: int, session: Session = Depends(db.get_session), user: UserInDB = Depends(get_current_user)):
    messagesInDB = db.get_messages_in_chat(session, chat_id)
    chatInDB = db.get_chat_by_id(session, chat_id)
    if user not in chatInDB.users:
        raise HTTPException(
            status_code = 403,
            detail={
                "error": "no_permission",
                "error_description": "requires permission to view chat"
            })
    messages = []
    for messageDB in messagesInDB:
        userInDB = messageDB.user
        messageUser = User(id=userInDB.id, username=userInDB.username, email=userInDB.email, created_at=userInDB.created_at)
        message = Message(id= messageDB.id, text= messageDB.text, chat_id= messageDB.chat_id, user= messageUser, created_at=messageDB.created_at)
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
def get_users(chat_id: int, session: Session = Depends(db.get_session), user: UserInDB = Depends(get_current_user)):
    usersInDB = db.get_users_in_chat(session, chat_id)
    chatInDB = db.get_chat_by_id(session, chat_id)
    if user not in chatInDB.users:
        raise HTTPException(
            status_code = 403,
            detail={
                "error": "no_permission",
                "error_description": "requires permission to view chat"
            })
    users = [User(id=user.id, username=user.username, email=user.email, created_at=user.created_at)
             for user in usersInDB]
    sort_key = lambda user: user.id
    return UserCollection(
        meta={"count": len(users)},
        users=sorted(users, key=sort_key),
    )

    

    



@chats_router.put("/{chat_id}/messages/{message_id}", 
                  response_model=MessageResponse,
                  description="Updates a message with the given message id.",)
def edit_message(chat_id: int, edited_message: NewMessage, message_id: int, userInDB: UserInDB = Depends(get_current_user),  session: Session = Depends(db.get_session)):
    """Update an chat for a given id."""

    msgInDb = db.update_message(session, chat_id, message_id, userInDB.id, edited_message)
    chatInDb = db.get_chat_by_id(session,chat_id)
    message_response = Message(id=msgInDb.id, text=edited_message.text, user_id=userInDB.id, chat_id=chat_id, user=userInDB,created_at=msgInDb.created_at,chat=chatInDb)
    return MessageResponse(
        message=message_response
    )

@chats_router.delete("/{chat_id}/messages/{message_id}", 
                    status_code=204,
                  description="Deletes a message with the given message id.",)
def delete_message(chat_id: int, message_id: int, userInDB: UserInDB = Depends(get_current_user),  session: Session = Depends(db.get_session)):
    """Update an chat for a given id."""

    db.delete_message(session, chat_id, message_id, userInDB.id)
    #chatInDb = db.get_chat_by_id(session,chat_id)
    #message_response = Message(id=msgInDb.id, text=edited_message.text, user_id=userInDB.id, chat_id=chat_id, user=userInDB,created_at=msgInDb.created_at,chat=chatInDb)
