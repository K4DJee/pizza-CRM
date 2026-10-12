from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.v1.routers.notification import router as notification_router
from exceptions import exceptions

app = FastAPI(title="Notification Service")
app.include_router(notification_router)

@app.get("/health")
async def health():
    return {"status": "Notification Service is running"}

@app.exception_handler(exceptions.SMTPRecipientRefused)
async def otp_error_sending_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=550,
        content={"detail": str(exc)},
    )

@app.exception_handler(exceptions.OTPErrorSending)
@app.exception_handler(exceptions.SMTPException)
@app.exception_handler(exceptions.SMTPAuthenticationError)
async def internal_server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )