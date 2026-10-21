
from fastapi import APIRouter, Response, Cookie, Depends, Request
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse
from httpclient import http_client
from exceptions import exceptions
from httpx import RequestError
from schemes import catalog
from config import config
from core.dependencies import require_role

router = APIRouter(tags=['Catalog'], prefix='/api/v1/catalog')
security = HTTPBearer()

@router.get("/")
async def proxy_get_catalog():
    try:
        response = await http_client.get(
            url=f"{config.CATALOG_SERVICE_URL}/api/v1/catalog"
        )

        try:
            content = response.json()
        except Exception:
            content = {"detail": response.text}

        client_response = JSONResponse(
            status_code=response.status_code,
            content=content
        )

        if client_response.status_code >= 400:
            return client_response

        return client_response

    except RequestError as e:
        raise exceptions.RequestError(f"Catalog Service недоступен: {str(e)}")

@router.post("/new")
async def proxy_add_new_catalog(
    data: catalog.CatalogCreateSchema,
    user_context = Depends(require_role(["kitchen", "admin"])) 
):
    try:
        response = await http_client.post(
            url=f"{config.CATALOG_SERVICE_URL}/api/v1/catalog/new",
            json=data.model_dump(mode='json')
        )

        try:
            content = response.json()
        except Exception:
            content = {"detail": response.text}

        client_response = JSONResponse(
            status_code=response.status_code,
            content=content
        )

        if client_response.status_code >= 400:
            return client_response

        return client_response

    except RequestError as e:
        raise exceptions.RequestError(f"Catalog Service недоступен: {str(e)}")

@router.delete("/{item_id}")
async def proxy_delete_catalog_item(
    item_id: int, 
    user_context = Depends(require_role(["kitchen", "admin"])) 
    ):
    try:
        response = await http_client.delete(
            url=f"{config.CATALOG_SERVICE_URL}/api/v1/catalog/{item_id}"
        )

        try:
            content = response.json()
        except Exception:
            content = {"detail": response.text}

        client_response = JSONResponse(
            status_code=response.status_code,
            content=content
        )

        if client_response.status_code >= 400:
            return client_response

        return client_response

    except RequestError as e:
        raise exceptions.RequestError(f"Catalog Service недоступен: {str(e)}")

@router.put("/{item_id}")
async def proxy_update_catalog_item(
    item_id: int, 
    data:catalog.CatalogCreateSchema,
    user_context = Depends(require_role(["kitchen", "admin"]))  
):
    try:
        response = await http_client.put(
            url=f"{config.CATALOG_SERVICE_URL}/api/v1/catalog/{item_id}",
            json=data.model_dump(mode='json')
        )

        try:
            content = response.json()
        except Exception:
            content = {"detail": response.text}

        client_response = JSONResponse(
            status_code=response.status_code,
            content=content
        )

        if client_response.status_code >= 400:
            return client_response

        return client_response

    except RequestError as e:
        raise exceptions.RequestError(f"Catalog Service недоступен: {str(e)}")
