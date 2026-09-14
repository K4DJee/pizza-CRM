from fastapi import APIRouter, HTTPException, status, Response, Depends
from ....services.catalog_service import get_catalog_catalog_service
from sqlalchemy.orm import Session
from ....db.session import get_db

router = APIRouter(tags=['Catalog'], prefix='/api/v1')

@router.get("/catalog")
async def get_catalog(
    db: Session = Depends(get_db)
):
    catalog = await get_catalog_catalog_service(db)
    return catalog