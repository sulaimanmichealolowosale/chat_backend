from pydantic import BaseModel, EmailStr, constr, conint
from typing import Optional, List
from enum import Enum


class Role(Enum):
    staff = "Staff"
    admin = "Admin"


class CreateUser(BaseModel):
    first_name: constr(strict=True, strip_whitespace=True)
    last_name: constr(strict=True, strip_whitespace=True)
    email: EmailStr
    staff_id: str
    role: str
    level: conint(ge=19)
    password: constr(strip_whitespace=True,
                     min_length=8, max_length=20)

class UpdateUser(BaseModel):
    first_name: constr(strict=True, strip_whitespace=True)
    last_name: constr(strict=True, strip_whitespace=True)
    email: EmailStr
    level: conint(ge=19)
    password: constr(strip_whitespace=True,
                     min_length=8, max_length=20)


class GetUsers(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    role: str
    level: str
    image_url: str
    staff_id: str

    class Config:
        orm_mode = True
