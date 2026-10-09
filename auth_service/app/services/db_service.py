from db.models.user import User
from sqlalchemy.orm import Session, selectinload, joinedload
from exceptions import exceptions

async def find_user_by_email(db: Session, email:str):
    user = db.query(User).filter(User.mail == email).first()
    return user

async def find_user_by_id(db: Session, user_id:int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise exceptions.UserNotFoundError("User not found")
    return user

async def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise exceptions.UserNotFoundError("User not found")

    db.delete(user)
    db.commit()

async def update_user_password(db: Session, user_id: int, hashed_password: str):
    user = await find_user_by_id(db, user_id)
    user.password = hashed_password
    db.commit()
