from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .user import GetUsers


class SendMessage(BaseModel):
    body: str


class GetMessage(BaseModel):
    id: int
    message_id: str
    # rev_message_id:str
    body: Optional[str] = None
    file_url: Optional[str] = None
    sender_id:str
    reciever_id:str
    sender: Optional[GetUsers] = []
    reciever: Optional[GetUsers] = []
    created_at: datetime

    class Config:
        orm_mode = True


class GetChat(BaseModel):
    id: int
    sender_fullname: Optional[str] = ""
    reciever_fullname: Optional[str] = ""
    sender_username: Optional[str] = ""
    reciever_username: Optional[str] = ""
    sender_username: Optional[str] = ""
    sender_image_url: Optional[str] = ""
    reciever_image_url: Optional[str] = ""
    sender_id: Optional[str] = ""
    reciever_id: Optional[str] = ""
    chat_id:Optional[str] = ""

    class Config:
        orm_mode = True
