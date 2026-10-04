from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .base import Base

# Сюда импортировать все модели, чтобы sqlalchemy видел их
from .models.user import User
from .models.catalog import Catalog
from .models.ingredient import Ingredient
from .models.composition import Composition

# SQLITE_DATABASE_URL = "sqlite:///./sql_app.db"
POSTGRES_DATABASE_URL="postgresql+psycopg://admin:root@localhost:5432/pizza_crm"

engine = create_engine(POSTGRES_DATABASE_URL, connect_args={}, pool_pre_ping=True)
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