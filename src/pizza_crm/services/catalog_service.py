from fastapi import Response, Depends
from sqlalchemy.orm import Session
from ..db.models.catalog import Catalog

async def get_catalog_catalog_service(db: Session):
    catalog = db.query(Catalog).all()

    return catalog