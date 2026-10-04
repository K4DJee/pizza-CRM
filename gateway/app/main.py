from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
from config import config
from .exceptions import exceptions
app = FastAPI(title="Pizza CRM API Gateway")

@app.get("/api/v1/auth/me")
async def proxy_get_user():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{config.AUTH_SERVICE_URL}/api/v1/auth/me",
                timeout=5.0
            )

        return response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, 
            detail=f"Auth Service недоступен: {str(e)}"
        )

@app.get("/health")
async def health_check():
    return {"status": "Gateway is running"}

@app.exception_handler(exceptions.RequestError)
async def request_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=503,
        content={"detail": str(exc)},
    )

# @app.exception_handler(exceptions.HTTPStatusError)
# async def request_error_handler(request: Request, exc: Exception):
#     return JSONResponse(
#         status_code=exc.,
#         content={"detail": str(exc)},
#     )
