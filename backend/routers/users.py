from fastapi import APIRouter
from datetime import date
from typing import Literal
from fastapi.exceptions import HTTPException
from backend.entities import (
    UserCreate,
    UserCollection,
    UserInDB,
    UserResponse,
    ChatCollection,
    ChatInDB
)
from backend import database as db

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.get("", 
                  response_model=UserCollection,
                  description="Get all users",)
def get_users():
    users = db.get_all_users()
    sort_key = lambda user: user.id
    return UserCollection(
        meta={"count": len(users)},
        users=sorted(users, key=sort_key),
    )


@users_router.post("", 
                   response_model=UserResponse,
                   description="Create a user",)
def create_user(user: UserCreate):
    
    # Need case for duplicate ID
    return UserResponse(user=db.create_user(user))

@users_router.get(
    "/{user_id}",
    response_model=UserResponse,
    description="Get a user for a given user id.",
)
def get_user(user_id: str):
    """Get an user for a given id."""

    return UserResponse(user=db.get_user_by_id(user_id))

@users_router.get(
    "/{user_id}/chats",
    response_model=ChatCollection,
    description="Returns chats for a user with the given id",
)
def get_user_chats(user_id: str):
    chats = db.get_chats_with_user(user_id)
    sort_key = lambda chat: chat.name
    return ChatCollection(
        meta={"count": len(chats)},
        chats=sorted(chats, key=sort_key),
    )
