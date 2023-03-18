from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt

from app.models.user import User
from .config import settings
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from .schemas.oauth2 import TokenData
from .database import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth")
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict, expire_time: timedelta = None):
    to_encode = data.copy()
    if expire_time:
        expire = datetime.utcnow()+expire_time
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('staff_id')

        if id is None:
            raise credentials_exception

        token_data = TokenData(id=id)

    except Exception:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
    token = verify_access_token(token, credentials_exception)

    user = db.query(User).filter(User.staff_id == token.id).first()

    return user


def get_current_admin_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
    token = verify_access_token(token, credentials_exception)

    user = db.query(User).filter(User.staff_id == token.id, User.role =="admin").first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform the requested action")

    return user
