from fastapi import APIRouter


router = APIRouter(tags=['Orders'], prefix='/api/v1')


@router.get("/orders/{}")
async def d():
    pass

