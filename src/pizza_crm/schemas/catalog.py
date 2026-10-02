from pydantic import BaseModel, ConfigDict
from decimal import Decimal
class CatalogResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    price: Decimal
    image_url: str
    is_active: bool

    composition: list[CompositionResponseSchema]

    model_config = ConfigDict(from_attributes=True) # разрешает маппинг из sqlalchemy

class CatalogCreateSchema(BaseModel):
    title: str
    description: str
    price: Decimal
    image_url: str
    is_active: bool

    composition: list[CompositionSchema]

    model_config = ConfigDict(from_attributes=True) # разрешает маппинг из sqlalchemy


class CompositionResponseSchema(BaseModel):
    quantity: int
    is_optional: bool
    ingredient: IngredientResponseSchema

    model_config = ConfigDict(from_attributes=True)

class CompositionSchema(BaseModel):
    quantity: int
    is_optional: bool
    ingredient: IngredientSchema

    model_config = ConfigDict(from_attributes=True)

class IngredientSchema(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)

class IngredientResponseSchema(BaseModel):
    id: int
    name: str
    unit: str
    cost_per_unit: Decimal
    is_allergen: bool

    model_config = ConfigDict(from_attributes=True)