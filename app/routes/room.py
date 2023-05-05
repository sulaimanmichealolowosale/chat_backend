# from typing import List
# from fastapi import APIRouter, Depends, status, HTTPException, Response, Response
# from sqlalchemy.orm import Session
# from ..models.message import Message
# from ..models.user import User
# from ..models.room import Room
# from ..models.perticipant import Perticipant
# from ..schemas.room import CreateRoom, GetRoom, GetMessageByRoom, GetPerticipantsByRoom, GetPerticipants
# from app.database import get_db
# from ..oauth2 import get_current_user
# from ..utils import check_not_found


# router = APIRouter(
#     tags=["Room"],
#     prefix="/api"
# )


# @router.post('/room', status_code=status.HTTP_201_CREATED, response_model=GetRoom)
# def manage_room(room: CreateRoom, db: Session = Depends(get_db),
#                 current_user: str = Depends(get_current_user)):

#     user = db.query(User).filter(User.staff_id ==
#                                  current_user.staff_id).first()

#     existing_room = db.query(Room).filter(Room.name == room.name).first()
#     if existing_room:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT,
#                             detail=f"A room with name {room.name} already exist please join the existing room instead")

#     new_room = Room(**room.dict(), created_by=user.staff_id)
#     db.add(new_room)
#     db.commit()
#     new_perticipant = Perticipant(room_id=new_room.id, first_name=user.first_name,
#                                   last_name=user.last_name, image_url=user.image_url, user_id=user.id)
#     db.add(new_perticipant)
#     db.commit()
#     db.refresh(new_room)
#     return new_room


# @router.post('/room/join/{room_id}', response_model=GetPerticipants)
# def manage_room(room_id: int, db: Session = Depends(get_db),
#                 current_user: str = Depends(get_current_user)):

#     user = db.query(User).filter(User.staff_id ==
#                                  current_user.staff_id).first()
#     room = db.query(Room).filter(Room.id == room_id).first()
#     check_not_found(room, room_id, check="room")

#     new_perticipant = Perticipant(room_id=room.id, first_name=user.first_name,
#                                   last_name=user.last_name, image_url=user.image_url, user_id=user.id)
#     db.add(new_perticipant)
#     db.commit()
#     db.refresh(new_perticipant)

#     return new_perticipant


# @router.get('/room', response_model=List[GetRoom])
# def manage_room(db: Session = Depends(get_db),
#                 current_user: str = Depends(get_current_user)):
#     rooms = db.query(Room).all()

#     return rooms


# @router.get('/room/chats/{room_id}', response_model=GetMessageByRoom)
# def manage_room(room_id: int, db: Session = Depends(get_db),
#                 current_user: str = Depends(get_current_user)):

#     room = db.query(Room).join(Message, Message.room_id == Room.id,
#                                isouter=True).filter(Room.id == room_id).first()

#     check_not_found(room, room_id, check="post")
#     return room


# @router.get('/room/perticipants/{room_id}', response_model=GetPerticipantsByRoom)
# def manage_room(room_id: int, db: Session = Depends(get_db),
#                 current_user: str = Depends(get_current_user)):

#     room = db.query(Room).join(Perticipant, Perticipant.room_id == Room.id,
#                                isouter=True).filter(Room.id == room_id).first()

#     check_not_found(room, room_id, check="room")
#     return room


# @router.put('/room/{room_id}/', response_model=GetRoom)
# def manage_room(room_id: int, room: CreateRoom, db: Session = Depends(get_db),
#                 current_user: str = Depends(get_current_user)):
#     room_query = db.query(Room).filter(Room.id == room_id)
#     room_result = room_query.first()

#     user = db.query(User).filter(User.staff_id ==
#                                  current_user.staff_id).first()
#     existing_room = db.query(Room).filter(Room.name == room.name).first()

#     if existing_room and existing_room.id != room_id:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT,
#                             detail=f"a room with the name {room.name} already exist")

#     check_not_found(room_result, room_id, check="room")
#     if user.staff_id != room_result.created_by:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                             detail="You are not allowed to perform the requested opreration")

#     room_query.update(room.dict(), synchronize_session=False)
#     db.commit()
#     return room_query.first()


# @router.delete('/room/{room_id}')
# def manage_room(room_id: int, db: Session = Depends(get_db),
#                 current_user: str = Depends(get_current_user)):
#     room_query = db.query(Room).filter(Room.id == room_id)
#     room_result = room_query.first()

#     user = db.query(User).filter(User.staff_id ==
#                                  current_user.staff_id).first()

#     check_not_found(room_result, room_id, check="room")
#     if user.staff_id != room_result.created_by:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                             detail="Ypu are not allowed to perform the requested opreration")

#     room_query.delete(synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @router.delete('/leave/room/{room_id}/{user_id}')
# def manage_room(user_id: int, room_id: int, db: Session = Depends(get_db),
#                 current_user: str = Depends(get_current_user)):

#     room = db.query(Room).filter(Room.id == room_id).first()
#     user = db.query(User).filter(User.staff_id ==
#                                  current_user.staff_id).first()
#     perticipant_query = db.query(Perticipant).filter(
#         Perticipant.room_id == room_id, Perticipant.user_id == user_id)

#     check_not_found(room, room_id, check="room")

#     perticipant_query.delete(synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
