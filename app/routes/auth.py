from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas.auth import GetAuthDetails
from ..database import get_db
from ..models.user import User
from ..utils import verify
from ..oauth2 import create_access_token
from datetime import timedelta


router = APIRouter(
    prefix="/api",
    tags=["Auth"]
)


@router.post('/auth', response_model=GetAuthDetails)
def auth(response: Response, login_details: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_details.username).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not verify(login_details.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = create_access_token(data={"staff_id": user.staff_id})
    refresh_token = create_access_token(
        data={"staff_id": user.staff_id}, expire_time=timedelta(days=1))

    response.set_cookie("refresh_token", refresh_token, httponly=True)
    response.set_cookie("access_token", access_token, httponly=True)
    return {"first_name": user.first_name, "last_name": user.last_name, "email": user.email, "staff_id": user.staff_id, "image_url": user.image_url, "role": user.role, "level": user.level, "access_token": refresh_token, "refresh_token": access_token}


@router.get('/logout')
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Loggged out"}
