from db.base import Base
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, func, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

class ReadyDish(Base):
    __tablename__ = "ready_dishes"

    id = Column(Integer, primary_key=True, index=True)
    catalog_id = Column(Integer, index=True)
    title = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    ready_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))
    prepared_by = Column(Integer)

    created_at = Column(DateTime(timezone=True), server_default=func.now())