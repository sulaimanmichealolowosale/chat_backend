from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from ..database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    staff_id = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    role = Column(String)
    password = Column(String, nullable=False)
    image_url = Column(String)
    verified = Column(Boolean, nullable=False, server_default=text("0"))
    level = Column(Integer, nullable=False)
    active = Column(Boolean, nullable=False, server_default=text("0"))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text('CURRENT_TIMESTAMP'))


