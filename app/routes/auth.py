from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas.auth import GetAuthDetails
from ..database import get_db
from ..models.user import User
from ..utils import verify
from ..oauth2 import create_access_token
from ..oauth2 import get_current_user
from datetime import timedelta


router = APIRouter(
    prefix="/api",
    tags=["Auth"]
)


@router.post('/auth', response_model=GetAuthDetails)
def auth(response: Response, login_details: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_query = db.query(User).filter(User.email == login_details.username)
    user_result = user_query.first()

    if user_result is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not verify(login_details.password, user_result.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = create_access_token(data={"staff_id": user_result.staff_id})
    refresh_token = create_access_token(
        data={"staff_id": user_result.staff_id}, expire_time=timedelta(days=1))

    user_query.update({"active": 1}, synchronize_session=False)
    db.commit()

    response.set_cookie("refresh_token", refresh_token, httponly=True)
    response.set_cookie("access_token", access_token, httponly=True)
    return {
        "first_name": user_result.first_name,
        "last_name": user_result.last_name,
        "email": user_result.email,
        "staff_id": user_result.staff_id,
        "image_url": user_result.image_url,
        "role": user_result.role,
        "active": user_result.active,
        "level": user_result.level,
        "access_token": refresh_token,
        "refresh_token": access_token
    }


@router.get('/logout')
def logout(response: Response, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    user_query = db.query(User).filter(User.staff_id == current_user.staff_id)
    user_result = user_query.first()

    user_query.update({"active": 0}, synchronize_session=False)
    db.commit()
    return {"message": "Loggged out"}
