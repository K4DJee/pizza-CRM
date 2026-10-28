from db.base import Base
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, func, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

class KitchenQueue(Base):
    __tablename__ = "kitchen_queue"

    id = Column(Integer, primary_key=True, index=True)
    order_item_id = Column(Integer, unique=True, index=True)
    order_id = Column(Integer, index=True)
    catalog_id = Column(Integer, index=True)
    title = Column(String(100), nullable=False)
    quanity = Column(Integer, nullable=False)
    modifications = Column(String(500))
    status = Column(
        String(20),
        CheckConstraint(
            "status IN ('queued', 'cooking', 'ready', 'cancelled')",
            name="check_task_status"
        ),
        nullable=False,
        default="queued"
    )
    prepared_at = Column(DateTime(timezone=True))
    prepared_by =Column(Integer, index=True)    
    started_at = Column(DateTime(timezone=True))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())