# from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql.sqltypes import TIMESTAMP
# from sqlalchemy.sql.expression import text
# from ..database import Base
# from .user import User
# from .perticipant import Perticipant


# class Room(Base):
#     __tablename__ = "rooms"
#     id = Column(Integer, primary_key=True, nullable=False)
#     name = Column(String, nullable=True)
#     description = Column(String, nullable=False, server_default="default room")
#     created_by = Column(String, ForeignKey("users.staff_id",
#                                            ondelete="CASCADE"), nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False,
#                         server_default=text("CURRENT_TIMESTAMP"))
#     creator = relationship("User")
#     messages = relationship("Message", back_populates='room')
#     perticipants = relationship("Perticipant")
