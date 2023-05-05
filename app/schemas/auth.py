from pydantic import BaseModel, EmailStr


class Auth(BaseModel):
    username: str
    password: str


class GetAuthDetails(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    role: str
    level: str
    image_url: str
    active: bool
    staff_id: str
    access_token: str
    refresh_token: str

    class Config:
        orm_mode = True


class Res(BaseModel):
    email: str

    class Config:
        orm_mode = True
