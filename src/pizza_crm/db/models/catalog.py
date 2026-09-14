from ...db.base import Base
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, func
from sqlalchemy.orm import relationship

class Catalog(Base):
    __tablename__ = "catalog"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    description = Column(String(250), nullable=False)
    price = Column(Numeric, nullable=False)
    image_url = Column(String(250), nullable=False)
    is_active = Column(Boolean, default=True)

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    composition = relationship("Composition", back_populates="dish", cascade="all, delete-orphan")


