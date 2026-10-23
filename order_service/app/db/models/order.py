from db.base import Base
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, func, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = "orders"

    # id = Column(Integer, primary_key=True, index=True)
    # user_id = Column(
    #     Integer, ForeignKey("users.id", ondelete="SET NULL"),
    #     nullable=True
    # )
    # status = Column(
    #     String(20),
    #     CheckConstraint(
    #         "status IN ('new', 'accepted', 'cooking', 'ready'",
    #         name="check_order_status"
    #     ),
    #     nullable=False,
    #     default="new"
    # )
    # total_amount = Column(Numeric, nullable=False)
    # comment = Column(String(500), nullable=True)
    # accepted_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    # created_at = Column(DateTime(timezone=True), server_default=func.now())
    # updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # user = relationship("User", back_populates="order")
    # transaction = relationship("Transaction", back_populates="order", uselist=False) #uselist отвечает за выдачу ответа: единичного или списка
    # items = relationship("OrderItem", back_populates="order")