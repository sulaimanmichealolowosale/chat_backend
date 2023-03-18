from passlib.context import CryptContext
from fastapi import HTTPException, status


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def password_hash(password):
    hashed_password = password_context.hash(password)
    return hashed_password


def verify(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def check_not_found(data, id, check=""):
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"A {check} with id: {id} was not found")
