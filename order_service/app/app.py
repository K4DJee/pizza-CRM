from fastapi import FastAPI

app = FastAPI(title="Auth Service")

@app.get("/api/v1/auth/me")
async def get_current_user():
    """Эндпоинт, который возвращает данные пользователя"""
    return {
        "user_id": 123,
        "email": "test@example.com",
        "role": "CUSTOMER"
    }

@app.get("/health")
async def health():
    return {"status": "Auth Service is running"}