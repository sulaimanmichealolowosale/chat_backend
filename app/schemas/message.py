from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .user import GetUsers


class SendMessage(BaseModel):
    body: str


class GetMessage(BaseModel):
    id: int
    body: str
    sender: GetUsers
    created_at: datetime

    class Config:
        orm_mode = True
