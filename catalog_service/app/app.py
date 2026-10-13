from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from exceptions import exceptions
from api.v1.routers.catalog import router as catalog_router

app = FastAPI(title="Catalog Service")

app.include_router(catalog_router)

@app.exception_handler(exceptions.DishNotFound)
async def user_not_found_exception_handler(request: Request, exc: exceptions.UserNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )

# @app.exception_handler(exceptions.InvalidTokenError)
# @app.exception_handler(exceptions.InvalidTokenPayload)
# async def invalid_token_handler(request: Request, exc:Exception):
#     return JSONResponse(
#         status_code=401,
#         content={"detail": str(exc)}
#     )

@app.exception_handler(exceptions.InvalidAuthHeader)
async def otp_error_sending(request: Request, exc:Exception):
    return JSONResponse(
        status_code=400,
        content={"detail":str(exc)}
    )

@app.exception_handler(exceptions.PermissionDenied)
async def forbidden(request: Request, exc: Exception):
    return JSONResponse(
        status_code=403, 
        content={"detail": str(exc)}
    )

@app.exception_handler(exceptions.IngredientNotExists)
async def server_error(request:Request, exc: Exception):
    return JSONResponse(
        status_code=404, 
        content={"detail":str(exc)}
    )

@app.exception_handler(exceptions.RequestError)
@app.exception_handler(exceptions.ErrorCreatingDish)
async def server_error(request:Request, exc: Exception):
    return JSONResponse(
        status_code=500, 
        content={"detail":str(exc)}
    )