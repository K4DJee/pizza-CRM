from ...db.base import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, func, Numeric, Boolean
from sqlalchemy.orm import relationship

class Ingredient(Base): # Ингредиенты
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(25), nullable=False, unique=True)
    unit = Column(String(20), default="г")
    cost_per_unit = Column(Numeric, nullable=False)
    is_allergen = Column(Boolean, nullable=False)

    composition_items = relationship("Composition", back_populates="ingredient")