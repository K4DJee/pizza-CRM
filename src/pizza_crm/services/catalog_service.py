from fastapi import Response, Depends
from sqlalchemy.orm import Session
from ..db.models.catalog import Catalog
from ..db.models.composition import Composition
from ..db.models.ingredient import Ingredient
from ..schemas import catalog
from ..exceptions import exceptions
from . import db_service
async def get_catalog_catalog_service(db: Session):
    catalog = await db_service.get_full_catalog(db)

    return catalog

async def delete_catalog_item_catalog_service(db: Session, item_id: int):
    await db_service.delete_catalog_item(db, item_id)

async def add_new_catalog_item_catalog_service(db: Session, new_item: catalog.CatalogCreateSchema):
    try:# нужно добавить ограничения в CatalogCreateSchema
        catalog_item = Catalog(
            title = new_item.title,
            description = new_item.description,
            price = new_item.price,
            image_url = new_item.image_url,
            is_active = new_item.is_active
        )

        db.add(catalog_item)
        db.flush()

        for comp_data in new_item.composition:
            ingredient = await db_service.find_ingredient_by_id(db, comp_data.ingredient.id)
            if not ingredient:
                db.rollback()
                raise exceptions.IngredientNotExists("Ingredient with this id doesn't exist. New dish not added.")

            composition = Composition(
                dish_id = catalog_item.id,
                ingredient_id = ingredient.id,
                quantity = comp_data.quantity,
                is_optional = comp_data.is_optional
            )
            db.add(composition)

        db.commit()
        
        db.refresh(catalog_item, attribute_names=["composition"])
        for comp in catalog_item.composition:
            db.refresh(comp, attribute_names=["ingredient"])
        return catalog_item
    except Exception as e:
        db.rollback()
        print(str(e))
        raise exceptions.ErrorCreatingDish("Error creating a dish")

async def update_catalog_item_catalog_service(db: Session, item_id: int,  new_item: catalog.CatalogCreateSchema):
    try:
        catalog_item = await db_service.find_catalog_item_by_id(db, item_id)
        if not catalog_item:
            raise exceptions.DishNotFound("Dish not found") 
        
        catalog_item.title = new_item.title
        catalog_item.description = new_item.description
        catalog_item.price = new_item.price
        catalog_item.image_url = new_item.image_url
        catalog_item.is_active = new_item.is_active

        await db_service.delete_compositions(db, item_id)

        db.flush()

        for comp_data in new_item.composition:
            ingredient = await db_service.find_ingredient_by_id(db, comp_data.ingredient.id)
            if not ingredient:
                db.rollback()
                raise exceptions.IngredientNotExists("Ingredient with this id doesn't exist. New dish not added.")

            composition = Composition(
                dish_id = catalog_item.id,
                ingredient_id = ingredient.id,
                quantity = comp_data.quantity,
                is_optional = comp_data.is_optional
            )
            db.add(composition)

        db.commit()
        db.refresh(catalog_item)
        return catalog_item
    except Exception as e:
        db.rollback()
        print(str(e))
        raise exceptions.ErrorCreatingDish("Error creating a dish")
