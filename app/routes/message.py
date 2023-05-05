from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Response, UploadFile, File, Response
from sqlalchemy.orm import Session
from ..models.message import Message, Chat
from ..models.user import User
from ..schemas.message import SendMessage, GetMessage, GetChat
from app.database import get_db
from sqlalchemy import desc
from ..oauth2 import get_current_user
from ..utils import check_not_found
import shutil


router = APIRouter(
    tags=["Message"],
    prefix="/api"
)


@router.post('/message/{reciever_id}', status_code=status.HTTP_201_CREATED, response_model=GetMessage)
def manage_chat(reciever_id: str, message: SendMessage, db: Session = Depends(get_db),
                current_user: str = Depends(get_current_user)):

    user = db.query(User).filter(User.staff_id ==
                                 current_user.staff_id).first()

    reciever = db.query(User).filter(User.staff_id == reciever_id).first()

    check_not_found(reciever, reciever_id, check="user")

    chat_query = db.query(Chat).filter(
        Chat.sender_id == reciever.staff_id, Chat.reciever_id == user.staff_id)

    chat_result = chat_query.first()

    if chat_result is not None:
        chat_query.delete(synchronize_session=False)
        db.commit()

    chat = db.query(Chat).filter(Chat.sender_id == user.staff_id,
                                 Chat.reciever_id == reciever.staff_id)
    existing_chat = chat.first()

    sender_fullname = user.first_name + " " + user.last_name
    sender_username = user.staff_id
    sender_image_url = user.image_url
    reciever_fullname = reciever.first_name + " " + reciever.last_name
    reciever_username = reciever.staff_id
    reciever_image_url = reciever.image_url

    message_id = user.staff_id+reciever.staff_id
    rev_message_id = reciever.staff_id+user.staff_id

    if existing_chat is not None:
        chat.delete(synchronize_session=False)
        new_chat = Chat(
            sender_fullname=sender_fullname,
            sender_username=sender_username,
            chat_id=message_id,
            sender_image_url=sender_image_url,
            reciever_fullname=reciever_fullname,
            reciever_username=reciever_username,
            reciever_image_url=reciever_image_url,
            sender_id=current_user.staff_id,
            reciever_id=reciever.staff_id
        )
        db.add(new_chat)
        db.commit()
    else:
        new_chat = Chat(
            sender_fullname=sender_fullname,
            sender_username=sender_username,
            chat_id=message_id,
            sender_image_url=sender_image_url,
            reciever_fullname=reciever_fullname,
            reciever_username=reciever_username,
            reciever_image_url=reciever_image_url,
            sender_id=current_user.staff_id,
            reciever_id=reciever.staff_id
        )
        db.add(new_chat)
        db.commit()

    existing_message_id = db.query(Message).filter(
        Message.message_id == rev_message_id).first()

    if existing_message_id is not None:
        new_message = Message(
            **message.dict(), reciever_id=reciever.staff_id, sender_id=user.staff_id, message_id=rev_message_id, rev_message_id=rev_message_id)
    else:
        new_message = Message(
            **message.dict(), reciever_id=reciever.staff_id, sender_id=user.staff_id, message_id=message_id, rev_message_id=rev_message_id)

    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


@router.post('/message/file/{reciever_id}', status_code=status.HTTP_201_CREATED, response_model=GetMessage)
def manage_chat(reciever_id: str, db: Session = Depends(get_db),
                current_user: str = Depends(get_current_user), file: UploadFile = File(...)):

    user = db.query(User).filter(User.staff_id ==
                                 current_user.staff_id).first()

    reciever = db.query(User).filter(User.staff_id == reciever_id).first()

    check_not_found(reciever, reciever_id, check="user")

    chat_query = db.query(Chat).filter(
        Chat.sender_id == reciever.staff_id, Chat.reciever_id == user.staff_id)

    chat_result = chat_query.first()

    if chat_result is not None:
        chat_query.delete(synchronize_session=False)
        db.commit()

    chat = db.query(Chat).filter(Chat.sender_id == user.staff_id,
                                 Chat.reciever_id == reciever.staff_id)
    existing_chat = chat.first()

    sender_fullname = user.first_name + " " + user.last_name
    sender_username = user.staff_id
    sender_image_url = user.image_url
    reciever_fullname = reciever.first_name + " " + reciever.last_name
    reciever_username = reciever.staff_id
    reciever_image_url = reciever.image_url

    with open("message_media/"+file.filename, "wb") as image:
        shutil.copyfileobj(file.file, image)
    file_url = "message_media/"+file.filename

    message_id = user.staff_id+reciever.staff_id
    rev_message_id = reciever.staff_id+user.staff_id

    if existing_chat is not None:
        chat.delete(synchronize_session=False)
        new_chat = Chat(
            sender_fullname=sender_fullname,
            sender_username=sender_username,
            chat_id=message_id,
            sender_image_url=sender_image_url,
            reciever_fullname=reciever_fullname,
            reciever_username=reciever_username,
            reciever_image_url=reciever_image_url,
            sender_id=current_user.staff_id,
            reciever_id=reciever.staff_id
        )
        db.add(new_chat)
        db.commit()
    else:

        new_chat = Chat(
            sender_fullname=sender_fullname,
            sender_username=sender_username,
            sender_image_url=sender_image_url,
            chat_id=message_id,
            reciever_fullname=reciever_fullname,
            reciever_username=reciever_username,
            reciever_image_url=reciever_image_url,
            sender_id=current_user.staff_id,
            reciever_id=reciever.staff_id
        )
        db.add(new_chat)
        db.commit()

    existing_message_id = db.query(Message).filter(
        Message.message_id == rev_message_id).first()
    # _existing_message_id = existing_message_id.message_id

    if existing_message_id is not None:
        new_message = Message(file_url=file_url, reciever_id=reciever.staff_id,
                              sender_id=user.staff_id, message_id=rev_message_id, rev_message_id=rev_message_id)
    else:
        new_message = Message(file_url=file_url, reciever_id=reciever.staff_id,
                              sender_id=user.staff_id, message_id=message_id, rev_message_id=rev_message_id)

    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


@router.get('/message/{sender_id}/{reciever_id}', response_model=List[GetMessage])
def manage_chat(sender_id: str, reciever_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    sender = db.query(User).filter(
        User.staff_id == sender_id).first()
    reciever = db.query(User).filter(User.staff_id == reciever_id).first()

    check_not_found(reciever, reciever_id, "user")

    message_id = sender_id+reciever_id

    messages = db.query(Message).filter(
        Message.message_id == message_id).all()

    return messages


@router.get('/message/{reciever_id}/{sender_id}', response_model=List[GetMessage])
def manage_chat(sender_id: str, reciever_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    reciever = db.query(User).filter(User.staff_id == reciever_id).first()

    check_not_found(reciever, reciever_id, "user")

    message_id = reciever_id+sender_id

    messages = db.query(Message).filter(
        Message.message_id == message_id).all()

    return messages


@router.get('/message/sent/all/chats', response_model=List[GetChat])
def manage_chat(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    chat = db.query(Chat).order_by(desc(Chat.created_at)).all()

    user_chats = []

    for chat in chat:
        if current_user.staff_id in chat.chat_id:
            user_chats.append(GetChat(
                id=chat.id,
                sender_fullname=chat.sender_fullname,
                reciever_username=chat.reciever_username,
                reciever_fullname=chat.reciever_fullname,
                sender_username=chat.sender_username,
                sender_image_url=chat.sender_image_url,
                reciever_image_url=chat.reciever_image_url,
                sender_id=chat.sender_id,
                reciever_id=chat.reciever_id,
                chat_id=chat.chat_id
            ))
    return user_chats


@router.get('/messages', response_model=List[GetMessage])
def manage_chat(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    chat = db.query(Message).filter(
        Message.reciever_id == current_user.staff_id).all()
    return chat


@router.delete('/message/{id}', status_code=status.HTTP_204_NO_CONTENT)
def manage_chat(id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    message_query = db.query(Message).filter(Message.id == id)

    message_result = message_query.first()
    check_not_found(message_result, id, "Message")
    message_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "message deleted successfully"}


@router.delete('/chat/del-chat/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def manage_chat(user_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = db.query(User).filter(User.staff_id ==
                                 current_user.staff_id).first()
    chat_query = db.query(Chat).filter(
        Chat.sender_id == user.staff_id, Chat.reciever_id == user_id)
    chat_result = chat_query.first()

    if chat_result == None:
        chat_query = db.query(Chat).filter(
            Chat.sender_id == user_id, Chat.reciever_id == user.staff_id)
        chat_result = chat_query.first()

    chat_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "chat deleted successfully"}
