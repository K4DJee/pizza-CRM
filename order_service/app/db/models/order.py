from db.base import Base
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, func, ForeignKey, CheckConstraint, null
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(20), index=True, nullable=False)
    user_id = Column(
        Integer, index=True,
        nullable=True
    )
    status = Column(
        String(20),
        CheckConstraint(
            "status IN ('new', 'accepted', 'cooking', 'ready', 'cancelled'",
            name="check_order_status"
        ),
        nullable=False,
        default="new"
    )
    total_amount = Column(Numeric, nullable=False)
    phone = Column(String(20), nullable=False)
    comment = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    transaction = relationship("Transaction", back_populates="order", uselist=False) #uselist отвечает за выдачу ответа: единичного или списка
    items = relationship("OrderItem", back_populates="order")