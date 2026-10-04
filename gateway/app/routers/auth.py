from fastapi import APIRouter

router = APIRouter(tags=['Authentication'], prefix='/api/v1')

# @router.post