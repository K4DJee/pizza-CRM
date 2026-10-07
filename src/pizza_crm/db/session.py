from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ..config import config
from .base import Base

# Сюда импортировать все модели, чтобы sqlalchemy видел их
from .models.user import User
from .models.catalog import Catalog
from .models.ingredient import Ingredient
from .models.composition import Composition

engine = create_engine(config.POSTGRES_DATABASE_URL, connect_args={}, pool_pre_ping=True)
# Base.metadata.create_all(bind=engine) - эта строка не нужна, тк используется alembic
print("tables created")
SessionLocal = sessionmaker(autoflush=False, bind=engine)

def get_db(): # позже надо сделать async
    db = SessionLocal()
    try:
        print("запрос db")
        yield db # raise 
    finally:
        db.close()