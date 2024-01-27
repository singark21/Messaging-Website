from fastapi import APIRouter
from datetime import date
from typing import Literal
from fastapi.exceptions import HTTPException
from backend.entities import (
    ChatInDB,
    ChatCollection,
    ChatResponse,
    ChatUpdate,
    MsgCollection,
    UserCollection
)
from backend import database as db
chats_router = APIRouter(prefix="/chats", tags=["Chats"])

@chats_router.get("", response_model=ChatCollection)
def get_chats():
    chats = db.get_all_chats()
    sort_key = lambda chat: chat.name
    return ChatCollection(
        meta={"count": len(chats)},
        chats=sorted(chats, key=sort_key),
    )

@chats_router.get(
    "/{chat_id}",
    response_model=ChatResponse,
    description="Get a user for a given user id.",
)
def get_chat(chat_id: str):
    """Get a chat for a given id."""

    return ChatResponse(chat=db.get_chat_by_id(chat_id))

@chats_router.put("/{chat_id}", response_model=ChatResponse)
def update_chat(chat_id: str, chat_update: ChatUpdate):
    """Update an chat for a given id."""

    return ChatResponse(
        chat=db.update_chat(chat_id, chat_update),
    )

@chats_router.delete(
    "/{chat_id}",
    status_code=204,
    response_model=None,
)
def delete_chat(chat_id: str) -> None:
    db.delete_chat(chat_id)


@chats_router.get(
    "/{chat_id}/messages",
    response_model=MsgCollection,
)
def get_msgs(chat_id: str):
    messages = db.get_messages_in_chat(chat_id)
    sort_key = lambda msg: msg.created_at
    return MsgCollection(
        meta={"count": len(messages)},
        messages=sorted(messages, key=sort_key),
    )

@chats_router.get(
    "/{chat_id}/users",
    response_model=UserCollection,
)
def get_users(chat_id: str):
    users = db.get_users_in_chat(chat_id)
    sort_key = lambda user: user.id
    return UserCollection(
        meta={"count": len(users)},
        users=sorted(users, key=sort_key),
    )



