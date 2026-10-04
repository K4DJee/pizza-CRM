import httpx

from config import config

http_client = httpx.AsyncClient(
    base_url=config.AUTH_SERVICE_URL, 
    timeout=5.0
)