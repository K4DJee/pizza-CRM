from db.base import Base
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, func, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship

class Transaction(Base):
    __tablename__ = "transactions"

    # id = Column(Integer, primary_key=True, index=True)
    # user_id = Column(
    #     Integer, ForeignKey("users.id", ondelete="SET NULL"),
    #     nullable=True
    # )
    # order_id = Column(
    #     Integer, ForeignKey("orders.id", ondelete="SET NULL"),
    #     nullable=True, unique=True
    # )
    # amount = Column(Numeric, nullable=False)
    # payment_method = Column(
    #     String(30),
    #     CheckConstraint(
    #         "payment_method IN ('card', 'cash', 'online', 'bonus')",
    #         name="check_payment_method"
    #     ),
    #     nullable=False
    # )
    # external_id = Column(String(100), nullable=True)
    # created_at = Column(DateTime(timezone=True), server_default=func.now())
    # updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # order = relationship("Order", back_populates="transaction")
    # user = relationship("User", foreign_keys=[user_id])