from fastapi import FastAPI
from src.pizza_crm.api.v1.routers.auth import router as auth_router
from src.pizza_crm.api.v1.routers.catalog import router as catalog_router
from fastapi.responses import RedirectResponse
app = FastAPI()

@app.get("/")
async def redirect_docs():
    return RedirectResponse("/docs")

app.include_router(auth_router)
app.include_router(catalog_router)