from fastapi import Response, Depends
from sqlalchemy.orm import Session
from ..db.models.catalog import Catalog
from .db_service import get_full_catalog, delete_catalog_item

async def get_catalog_catalog_service(db: Session):
    catalog = await get_full_catalog(db)

    return catalog

async def delete_catalog_item_catalog_service(db: Session, item_id: int):
    await delete_catalog_item(db, item_id)