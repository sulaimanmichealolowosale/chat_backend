from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .user import GetUsers
from .message import GetMessage


class CreateRoom(BaseModel):
    name: str
    description: str


class GetRoom(BaseModel):
    id: int
    name: str
    created_by:str
    description: Optional[str] = ''
    creator: Optional[GetUsers] = []
    created_at: datetime

    class Config:
        orm_mode = True


class GetMessageByRoom(GetRoom):
    messages: List[GetMessage] = []


class GetPerticipants(BaseModel):
    id: int
    first_name:str
    last_name:str
    image_url:str
    user_id: int
    room_id: int
    date_joined: datetime

    class Config:
        orm_mode = True


class GetPerticipantsByRoom(GetRoom):
    perticipants: List[GetPerticipants] = []
