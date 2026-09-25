from fastapi import FastAPI, Request
from src.pizza_crm.api.v1.routers.auth import router as auth_router
from src.pizza_crm.api.v1.routers.catalog import router as catalog_router
from fastapi.responses import RedirectResponse, JSONResponse
from src.pizza_crm.exceptions import exceptions
app = FastAPI()

@app.get("/")
async def redirect_docs():
    return RedirectResponse("/docs")
app.include_router(auth_router)
app.include_router(catalog_router)

#способ с глобальными обработчиками
@app.exception_handler(exceptions.UserNotFoundError)
@app.exception_handler(exceptions.OTPNotFound)
@app.exception_handler(exceptions.ResetTokenNotFound)
@app.exception_handler(exceptions.DishNotFound)
async def user_not_found_exception_handler(request: Request, exc: exceptions.UserNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )

@app.exception_handler(exceptions.InvalidTokenError)
@app.exception_handler(exceptions.InvalidTokenPayload)
async def invalid_token_handler(request: Request, exc:Exception):
    return JSONResponse(
        status_code=401,
        content={"detail": str(exc)}
    )

@app.exception_handler(exceptions.OTPExists)
@app.exception_handler(exceptions.OTPNotMatch)
@app.exception_handler(exceptions.OTPErrorSending)
@app.exception_handler(exceptions.ReetTokenExists)
@app.exception_handler(exceptions.ResetTokenNotMatch)
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