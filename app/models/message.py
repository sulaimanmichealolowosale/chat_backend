from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from ..database import Base
from .user import User


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, nullable=False)
    body = Column(String, nullable=False, server_default="file")
    file_url = Column(String, nullable=True)
    sender_id = Column(String, ForeignKey("users.staff_id",
                                          ondelete="CASCADE"), nullable=False)
    reciever_id = Column(String, ForeignKey("users.staff_id",
                                            ondelete="CASCADE"), nullable=False)
    message_id = Column(String, nullable=False)
    rev_message_id = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    sender = relationship("User", foreign_keys=sender_id)
    reciever = relationship("User", foreign_keys=reciever_id)


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, nullable=False, primary_key=True)
    sender_fullname = Column(String, nullable=True)
    reciever_fullname = Column(String, nullable=True)
    reciever_username = Column(String, nullable=True)
    sender_username = Column(String, nullable=True)
    sender_image_url = Column(String, nullable=True)
    reciever_image_url = Column(String, nullable=True)
    sender_id = Column(String, ForeignKey("users.staff_id",
                                          ondelete="CASCADE"), nullable=False)
    reciever_id = Column(String, ForeignKey("users.staff_id",
                                            ondelete="CASCADE"), nullable=False)
    chat_id = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
