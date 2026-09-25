from sqlalchemy import Column, Integer, String,DateTime, func, CheckConstraint, Enum
from ..base import Base
import enum

# class UserRole(str, enum.Enum):
#     CUSTOMER = "customer"
#     KITCHEN = "kitchen"
#     ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    surname = Column(String(250), nullable=False)
    patronymic = Column(String(250), nullable=True)
    age = Column(Integer, CheckConstraint('age >= 0 AND age <= 120'), nullable=False)
    password = Column(String, nullable=False) # нужно поставить ограничения
    role = Column(
        String(20),
        CheckConstraint("role IN ('customer', 'kitchen', 'admin')", name='check_role'),
        nullable=False,
        default='customer'
    )
    # refreshToken = Column(String, nullable=False)
    mail = Column(String(50), nullable=False, unique=True) # нужно поставить ограничения
    createdAt = Column(DateTime(timezone=True), server_default=func.now()) # поменять на нижнее подчеркивание
    updatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

