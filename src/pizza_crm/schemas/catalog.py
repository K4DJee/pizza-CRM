from pydantic import BaseModel, ConfigDict
from decimal import Decimal
class CatalogSchema(BaseModel):
    id: int
    title: str
    description: str
    price: Decimal

    composition: list[CompositionSchema]

    model_config = ConfigDict(from_attributes=True) # разрешает маппинг из sqlalchemy

class CompositionSchema(BaseModel):
    quantity: int
    is_optional: bool
    ingredient: IngredientSchema

    model_config = ConfigDict(from_attributes=True)

class IngredientSchema(BaseModel):
    id: int
    name: str
    unit: str
    cost_per_unit: Decimal
    is_allergen: bool

    model_config = ConfigDict(from_attributes=True)