from ..base import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class Composition(Base): # Состав
    __tablename__ = "composition"

    dish_id = Column(Integer, ForeignKey("catalog.id", ondelete="CASCADE"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id", ondelete="CASCADE"), primary_key=True)

    quantity = Column(Integer, nullable=False)
    is_optional = Column(Boolean, nullable=False) # можно ли убрать ингредиент

    dish = relationship("Catalog", back_populates="composition")
    ingredient = relationship("Ingredient", back_populates="composition_items")