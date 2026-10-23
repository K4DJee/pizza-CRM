from db.base import Base
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, func, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

class KitchenQueue(Base):
    __tablename__ = "kitchen_queue"

    id = Column(Integer, primary_key=True, index=True)
    

    # created_at = Column(DateTime(timezone=True), server_default=func.now())
    # updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # prepaper = relationship("User", foreign_keys=[prepared_by])
    # order = relationship("Order", back_populates="items")
    # catalog_item = relationship("Catalog")