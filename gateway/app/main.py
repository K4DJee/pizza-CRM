from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
from config import config
from exceptions import exceptions
from routers.auth import router as auth_router
from routers.catalog import router as catalog_router
app = FastAPI(title="Pizza CRM API Gateway")

app.include_router(auth_router)
app.include_router(catalog_router)


@app.get("/health")
async def health_check():
    return {"status": "Gateway is running"}

@app.exception_handler(exceptions.RequestError)
async def request_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=503,
        content={"detail": str(exc)},
    )


@app.exception_handler(exceptions.InternalServerError)
async def internal_server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )
# @app.exception_handler(exceptions.HTTPStatusError)
# async def request_error_handler(request: Request, exc: Exception):
#     return JSONResponse(
#         status_code=exc.,
#         content={"detail": str(exc)},
#     )

@app.exception_handler(exceptions.PermissionDenied)
async def forbidden(request: Request, exc: Exception):
    return JSONResponse(
        status_code=403, 
        content={"detail": str(exc)}
    )