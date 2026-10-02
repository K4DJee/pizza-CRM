from ..db.models.user import User
from ..db.models.catalog import Catalog
from ..db.models.composition import Composition
from ..db.models.ingredient import Ingredient 
from sqlalchemy.orm import Session, selectinload, joinedload
from ..exceptions import exceptions

async def find_user_by_email(db: Session, email:str):
    user = db.query(User).filter(User.mail == email).first()
    return user

async def find_user_by_id(db: Session, user_id:int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise exceptions.UserNotFoundError("User not found")
    return user

async def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise exceptions.UserNotFoundError("User not found")

    db.delete(user)
    db.commit()

async def update_user_password(db: Session, user_id: int, hashed_password):
    user = await find_user_by_id(db, user_id)
    user.password = hashed_password
    db.commit()

async def get_full_catalog(db: Session):
    catalog_items = db.query(Catalog).options(
        selectinload(Catalog.composition).joinedload(Composition.ingredient)
    )
    return catalog_items

async def delete_catalog_item(db: Session, item_id: int):
    catalog_item = db.query(Catalog).filter(Catalog.id == item_id).first()
    if not catalog_item:
        raise exceptions.DishNotFound("Dish not found")
    db.delete(catalog_item)
    db.commit()

async def find_ingredient_by_id(db: Session, id: int) -> Ingredient:
    ingredient = db.query(Ingredient).filter(Ingredient.id == id).first()
    return ingredient

async def find_catalog_item_by_id(db: Session, id: int) -> Catalog:
    catalog_item = db.query(Catalog).filter(Catalog.id == id).first()
    return catalog_item

async def delete_compositions(db: Session, dish_id):
    db.query(Composition).filter(Composition.dish_id == dish_id).delete()
    return