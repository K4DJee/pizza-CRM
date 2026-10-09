from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .base import Base
from config import config

# Сюда импортировать все модели, чтобы sqlalchemy видел их
from .models.user import User

# POSTGRES_DATABASE_URL="postgresql+psycopg://admin:root@localhost:5432/pizza_crm"

engine = create_engine(config.DATABASE_URL, connect_args={}, pool_pre_ping=True)
# Base.metadata.create_all(bind=engine) - эта строка не нужна, тк используется alembic
SessionLocal = sessionmaker(autoflush=False, bind=engine)

def get_db(): # позже надо сделать async
    db = SessionLocal()
    try:
        print("запрос db")
        yield db # raise 
    finally:
        db.close()