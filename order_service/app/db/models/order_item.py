from db.base import Base
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, func, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

class OrderItem(Base):
    __tablename__ = "order_items"

    # id = Column(Integer, primary_key=True, index=True)
    # order_id = Column(
    #     Integer, ForeignKey("orders.id", ondelete="CASCADE"),
    #     nullable=False
    # )
    # catalog_id =  Column(
    #     Integer, ForeignKey("catalog.id", ondelete="SET NULL"),
    #     nullable=True  # SET NULL — чтобы блюдо осталось в истории, даже если его удалят из каталога
    # )
    # quantity = Column(Integer, nullable=False, default=1)
    # price_at_order = Column(Numeric, nullable=False)
    # status = Column(
    #     String(20),
    #     CheckConstraint(
    #         "status IN ('new', 'cooking', 'ready', 'cancelled')",
    #         name="check_item_status"
    #     ),
    #     nullable=False,
    #     default="new"
    # )
    # prepared_by = Column(
    #     Integer, ForeignKey("users.id", ondelete="SET NULL"),
    #     nullable=True
    # )
    # modifications = Column(String(500), nullable=True)

    # created_at = Column(DateTime(timezone=True), server_default=func.now())
    # updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # prepaper = relationship("User", foreign_keys=[prepared_by])
    # order = relationship("Order", back_populates="items")
    # catalog_item = relationship("Catalog")