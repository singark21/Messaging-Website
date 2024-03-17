from fastapi import APIRouter, Depends
from datetime import date
from typing import Literal
from fastapi.exceptions import HTTPException
from backend.auth import get_current_user
from backend.entities import (
    UserCreate,
    UserCollection,
    UserInDB,
    UserResponse,
    UserUpdate,
    User,
    ChatCollection,
    ChatInDB,
    Chat,
)
from backend import database as db
from sqlmodel import Session

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.get("", 
                  response_model=UserCollection,
                  description="Get all users",)

def get_users(session: Session = Depends(db.get_session)):
    usersInDB = db.get_all_users(session)
    sort_key = lambda user: user.id

    users = [User(id=user.id, username=user.username, email=user.email, created_at=user.created_at)
             for user in usersInDB]
    return UserCollection(
        meta={"count": len(users)},
        users=sorted(users, key=sort_key),
    )


@users_router.get(
    "/{user_id}",
    response_model=UserResponse,
    description="Get a user for a given user id.",
)
def get_user(user_id: int, session: Session = Depends(db.get_session)):
    """Get an user for a given id."""
    userInDB = db.get_user_by_id(session,user_id)
    userResponse = User(id=userInDB.id, username=userInDB.username, email=userInDB.email, created_at=userInDB.created_at)
    return UserResponse(user = userResponse)



@users_router.get(
    "/{user_id}/chats",
    response_model=ChatCollection,
    description="Returns chats for a user with the given id",
)
def get_user_chats(user_id: int, session: Session = Depends(db.get_session)):
    chatsInDB = db.get_chats_with_user(session, user_id)
    sort_key = lambda chat: chat.name
    
    chats_response = []
    for chat in chatsInDB:
        owner = get_user(chat.owner.id,session)
        chat_response = Chat(id=chat.id, name=chat.name, owner=owner.user, created_at=chat.created_at)
        chats_response.append(chat_response)

    return ChatCollection(
        meta={"count": len(chats_response)},
        chats=sorted(chats_response, key=sort_key),
    )




@users_router.get(
    "/me",
    response_model=UserResponse,
    description="Get the current user.",
)
def get_self(user: UserInDB = Depends(get_current_user)):
    return UserResponse(user = user)

@users_router.put(
    "/me",
    response_model=UserResponse,
    description="Update the current user.",
)
def update_self(user: UserInDB = Depends(get_current_user), user_update = UserUpdate, session: Session = Depends(db.get_session)):
    updatedUser = db.update_user(session, user, user_update) 
    userResponse = User(id=updatedUser.id, username=updatedUser.username, email=updatedUser.email, created_at=updatedUser.created_at)
    return UserResponse(user = userResponse)