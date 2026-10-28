from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .base import Base
from config import config

# Сюда импортировать все модели, чтобы sqlalchemy видел их
from db.models.kitchen_queue import KitchenQueue
from db.models.ready_dish import ReadyDish

engine = create_engine(config.DATABASE_KITCHEN_URL, connect_args={}, pool_pre_ping=True)
# Base.metadata.create_all(bind=engine) - эта строка не нужна, тк используется alembic
SessionLocal = sessionmaker(autoflush=False, bind=engine)

def get_db(): # позже надо сделать async
    db = SessionLocal()
    try:
        print("запрос db")
        yield db # raise 
    finally:
        db.close()