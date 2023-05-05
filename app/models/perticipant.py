# from sqlalchemy import Column, Integer, ForeignKey, String
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql.sqltypes import TIMESTAMP
# from sqlalchemy.sql.expression import text
# from ..database import Base


# class Perticipant(Base):
#     __tablename__ = "perticipants"
#     id = Column(Integer, primary_key=True, nullable=False)
#     room_id = Column(Integer, ForeignKey(
#         "rooms.id", ondelete="CASCADE"), nullable=False)
#     first_name = Column(String, nullable=True, server_default="first_name")
#     last_name = Column(String, nullable=True, server_default="last_name")
#     image_url = Column(String, nullable=True)
#     user_id = Column(Integer, ForeignKey(
#         "users.id", ondelete="CASCADE"), nullable=False)
#     date_joined = Column(TIMESTAMP(timezone=True), nullable=False,
#                          server_default=text("CURRENT_TIMESTAMP"))
