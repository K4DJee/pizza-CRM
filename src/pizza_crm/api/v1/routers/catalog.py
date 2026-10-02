from fastapi import APIRouter, HTTPException, status, Response, Depends
from ....services import catalog_service
from sqlalchemy.orm import Session
from ....db.session import get_db
from ....api.dependencies import require_role
from ....schemas.catalog import CatalogResponseSchema, CatalogCreateSchema

router = APIRouter(tags=['Catalog'], prefix='/api/v1')

@router.get("/catalog", response_model=list[CatalogResponseSchema])
async def get_catalog(
    db: Session = Depends(get_db)
):
    catalog = await catalog_service.get_catalog_catalog_service(db)
    return catalog

@router.post("/catalog/new", response_model=CatalogResponseSchema)
async def add_new_catalog(
    new_item: CatalogCreateSchema,
    db: Session = Depends(get_db),
    user_context = Depends(require_role(["kitchen", "admin"])) 
):
    catalog_item = await catalog_service.add_new_catalog_item_catalog_service(db, new_item)
    return catalog_item

@router.delete("/catalog/{item_id}")
async def delete_catalog_item(
    item_id: int, 
    db: Session = Depends(get_db),
    user_context = Depends(require_role(["kitchen", "admin"])) 
    ):
    await catalog_service.delete_catalog_item_catalog_service(db, item_id)
    return {"message": "Dish was deleted from catalog"}

@router.post("/catalog/{item_id}/update")
async def add_new_catalog(
    item_id: int, 
    new_item:CatalogCreateSchema, 
    db: Session = Depends(get_db),
    user_context = Depends(require_role(["kitchen", "admin"])) 
):
    catalog_item = await catalog_service.update_catalog_item_catalog_service(db, item_id, new_item)
    return {"message": "Dish was updated", "catalog_item": catalog_item}

