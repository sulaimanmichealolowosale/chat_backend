import shutil
from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File, Response
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.user import CreateUser, GetUsers, UpdateUser
from ..models.user import User
from ..utils import password_hash, check_not_found
from ..oauth2 import get_current_user, get_current_admin_user

router = APIRouter(
    tags=["Users"],
    prefix="/user"
)


@router.post('/', response_model=GetUsers, status_code=status.HTTP_201_CREATED)
def manage_users(user: CreateUser = Depends(), file: UploadFile = File(...), db:
                 Session = Depends(get_db), current_user: str = Depends(get_current_admin_user)):

    hashed_password = password_hash(user.password)
    user.password = hashed_password

    existing_user = db.query(User).filter(User.email == user.email).first()
    existing_staff_id = db.query(User).filter(
        User.staff_id == user.staff_id).first()

    if existing_staff_id is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"The user with email {user.staff_id} already exist")

    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"The user with staff_id {user.email} already exist")

    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"the file: {file.filename} is not an image file")

    with open("media/"+file.filename, "wb") as image:
        shutil.copyfileobj(file.file, image)
    image_url = "media/"+file.filename

    new_user = User(image_url=image_url, **user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/', response_model=List[GetUsers])
def manage_users(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    users = db.query(User).all()
    return users


@router.get('/{id}', response_model=GetUsers)
def manage_users(id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = db.query(User).filter(User.staff_id == id).first()

    check_not_found(user, id, "user")
    return user


@router.put('/{id}', response_model=GetUsers)
def manage_users(id: str, user: UpdateUser = Depends(), file: UploadFile = File(...),
                 db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):

    user_query = db.query(User).filter(User.staff_id == id)
    user_result = user_query.first()

    existing_email = db.query(User).filter(User.email == user.email).first()

    if existing_email and id != existing_email.staff_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already taken")

    check_not_found(user_result, id, "user")

    hashed_password = password_hash(user.password)
    user.password = hashed_password

    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"the file: {file.filename} is not an image file")

    with open("media/"+file.filename, "wb") as image:
        shutil.copyfileobj(file.file, image)
    image_url = "media/"+file.filename

    user_dict = user.dict()
    user_dict['image_url'] = image_url

    user_query.update(user_dict, synchronize_session=False)
    db.commit()
    return user_query.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def manage_users(id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_admin_user)):
    user_query = db.query(User).filter(User.staff_id == id)
    user_result = user_query.first()

    check_not_found(user_result, id, "user")
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
