from fastapi import APIRouter, HTTPException, status, Response, Depends
from ....services import catalog_service
from sqlalchemy.orm import Session
from ....db.session import get_db
from ....api.dependencies import require_role
from ....schemas.catalog import CatalogSchema

router = APIRouter(tags=['Catalog'], prefix='/api/v1')

@router.get("/catalog", response_model=list[CatalogSchema])
async def get_catalog(
    db: Session = Depends(get_db)
):
    catalog = await catalog_service.get_catalog_catalog_service(db)
    return catalog

@router.post("/catalog/new")
async def add_new_catalog():
    pass

@router.delete("/catalog/{item_id}")
async def delete_catalog_item(
    item_id: int, 
    db: Session = Depends(get_db),
    user_context = Depends(require_role(["kitchen", "admin"])) 
    ):
    await catalog_service.delete_catalog_item(db, item_id)
    return {"message": "Dish was deleted from catalog"}

@router.post("/catalog/update")
async def add_new_catalog():
    pass

