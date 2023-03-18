from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from ..database import Base
from .user import User


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, nullable=False)
    body = Column(String, nullable=False)
    sender_id = Column(String, ForeignKey("users.staff_id",
                                          ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    sender=relationship("User")
