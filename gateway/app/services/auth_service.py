from fastapi import HTTPException
from httpclient import http_client
from ..exceptions.exceptions import exceptions
import httpx

async def _proxy_request(method: str, path: str, body: dict = None) -> dict:
    """
    Делает запрос к Auth Service. Обрабатывает ошибки сети и HTTP-статусы.
    """
    try:
        response = await http_client.request(method, path, json=body)
        response.raise_for_status()  # Проверка на 4xx и 5xx
        return response.json()
    
    except httpx.RequestError as e:
        raise exceptions.RequestError(f"Auth Service недоступен: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, 
            detail=e.response.text
        )

