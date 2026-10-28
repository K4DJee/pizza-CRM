from db.base import Base
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, func, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(
        Integer, ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False
    )
    catalog_id =  Column(
        Integer, index=True,
        nullable=False
    )
    title_snapshot = Column(String(100), nullable=False)# 
    quantity = Column(Integer, nullable=False, default=1)
    price_at_order = Column(Numeric, nullable=False)
    modifications = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    order = relationship("Order", back_populates="items")