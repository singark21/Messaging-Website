from datetime import date, datetime

from pydantic import BaseModel, Field


class ChatInDB(BaseModel):
    """Represents a chat in the database."""

    id: str
    name: str
    user_ids: list[str]
    owner_id: str
    created_at: datetime


class UserInDB(BaseModel):
    """Represents a user in the database."""

    id: str
    created_at: datetime

class UserCreate(BaseModel):
    """Represents parameters for adding a new user to the system."""

    id: str
    
class UserResponse(BaseModel):
    """Represents an API response for an user."""

    user: UserInDB

class Metadata(BaseModel):
    """Represents metadata for a collection."""

    count: int

class UserCollection(BaseModel):
    """Represents an API response for a collection of users."""

    meta: Metadata
    users: list[UserInDB]

class ChatInDB(BaseModel):
    """Represents a user in the database."""

    id: str
    name: str
    user_ids: list[str]
    owner_id: str
    created_at: datetime

class MsgInDB(BaseModel):
    id: str
    user_id: str
    text: str
    created_at: datetime

class MsgCollection(BaseModel):
    meta: Metadata
    messages: list[MsgInDB]

class ChatCollection(BaseModel):
    """Represents an API response for a collection of chats."""

    meta: Metadata
    chats: list[ChatInDB]

class ChatResponse(BaseModel):
    """Represents an API response for an user."""

    chat: ChatInDB

class ChatUpdate(BaseModel):
    """Represents parameters for updating an chat in the system."""

    name: str 
    
