from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from exceptions import exceptions
from api.v1.routers.order import router as order_router

app = FastAPI(title="Order Service")

app.include_router(order_router)

@app.exception_handler(exceptions.InternalServerError)
async def server_error(request:Request, exc: Exception):
    return JSONResponse(
        status_code=500, 
        content={"detail":str(exc)}
    )