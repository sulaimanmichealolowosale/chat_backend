from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Response, Body
from sqlalchemy.orm import Session
from ..models.message import Message
from ..models.user import User
from ..schemas.message import SendMessage, GetMessage
from app.database import get_db
from ..oauth2 import get_current_user
from ..utils import check_not_found


router = APIRouter(
    tags=["Message"],
    prefix="/api"
)


@router.post('/message', status_code=status.HTTP_201_CREATED, response_model=GetMessage)
def manage_chat(message: SendMessage, db: Session = Depends(get_db),
                current_user: str = Depends(get_current_user)):

    user = db.query(User).filter(User.staff_id ==
                                 current_user.staff_id).first()

    new_message = Message(**message.dict(), sender_id=user.staff_id)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


@router.get('/message', response_model=List[GetMessage])
def manage_chat(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    messages = db.query(Message).all()
    return messages


@router.delete('/message/{id}', status_code=status.HTTP_204_NO_CONTENT)
def manage_chat(id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    message_query = db.query(Message).filter(Message.id == id)
    if current_user.role == "staff":
        message_query = db.query(Message).filter(
            Message.id == id, Message.sender_id == current_user.staff_id)

    message_result = message_query.first()
    check_not_found(message_result, id, "Message")
    message_query.delete(synchronize_session=False)
    db.commit()
    return {"message":"message deleted successfully"}