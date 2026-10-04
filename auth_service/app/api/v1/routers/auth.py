from sqlalchemy.orm import Session
from ..schemas.user import RegisterUserRequest, LoginUserRequest
from ..db.models.user import User
from sqlalchemy.exc import IntegrityError
import bcrypt
import datetime
import jwt
from ..models.tokens import Tokens
from ..db.models.tokens import Token
from ..config import config
from . import db_service, redis_service, notifications_service
from ....exceptions import exceptions


async def register_auth_service(db: Session, data: RegisterUserRequest) -> User:
    existing_user = await db_service.find_user_by_email(db, data.email)
    if existing_user:
        raise ValueError("User with this mail is exists")

    hashed_password = hash_password(data.password)

    new_user = User(
        name=data.name,
        surname = data.surname,
        patronymic = data.patronymic,
        age = data.age,
        mail = data.email,
        password = hashed_password
    )

    db.add(new_user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("User with this email already exists")

    db.refresh(new_user)
    return new_user

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')