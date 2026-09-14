from fastapi import FastAPI, APIRouter, HTTPException, status, Depends, Request, Response, Cookie
from sqlalchemy.orm import Session
from ....services.auth_service import register_auth_service, login_auth_service, create_tokens_pair, save_refresh_token_to_db, verify_token, get_userdata
from ....schemas.user import RegisterUserRequest, LoginUserRequest, UserResponse
from ....db.session import get_db  
from ....config import config
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(tags=['Authentication'], prefix='/api/v1')

security = HTTPBearer()

@router.post("/register")
async def register(
    data: RegisterUserRequest,
    db: Session = Depends(get_db)
):
    try:
        print(data)
        new_user = await register_auth_service(db, data)
        return {"message": "User registered", "user_id": new_user.id}
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))

@router.post("/login")
async def login(
    data: LoginUserRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    try:
        print(data)
        user = await login_auth_service(db, data)
        # Выдача accessToken и refreshToken
        tokens = create_tokens_pair(str(user.id))
        user_agent = request.headers.get("user-agent", "unknown")

        response.set_cookie(
            key="refresh_token",
            value=tokens.RefreshToken,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=config.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        )
        await save_refresh_token_to_db(db, user.id, tokens.RefreshToken, user_agent)


        return {"AccessToken":tokens.AccessToken, "RefreshToken":tokens.RefreshToken, "message":"You have successfully logged in"}

    except ValueError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(e))

@router.post("/refresh")
async def refresh_tokens(request: Request, response: Response, refresh_token: str = Cookie(None),
    db: Session = Depends(get_db)):
    if not refresh_token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Refresh token not found")

    try:
        payload = verify_token(refresh_token, config.JWT_REFRESH_SECRET_KEY)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token payload")
    except ValueError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(e))

      # 3. Генерируем  Access Token и refresh
    tokens = create_tokens_pair(user_id)
    user_agent = request.headers.get("user-agent", "unknown")

      # 4.Обновляем куки с новым refresh токеном
    response.set_cookie(
        key="refresh_token",
        value=tokens.RefreshToken,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=config.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )

    await save_refresh_token_to_db(db, user_id, tokens.RefreshToken, user_agent)

      # 5. Возвращаем новый Access Token
    return{"AccessToken": tokens.AccessToken}
    

@router.put("/change-password")
async def change_password(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    # клиент отправляет почту серверу
    # сервер проверяет наличие аккаунта с данной почтой
    # сервер генерирует через redis и отправляет код на почту
    # клиент получает код и отправляет его серверу
    # сервер проверяет корректность пароля и перенаправляет пользователя на endpoint со сменой пароля

    # redis using
    pass

@router.get("/me", response_model=UserResponse)
async def get_profile(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    try:
        payload = verify_token(token, config.JWT_ACCESS_SECRET_KEY)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token payload")
    
        # даём данные пользователя
        user = get_userdata(int(user_id), db)
        return user # reponse_model сама уберёт лишний пароль 
    except ValueError as e:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(e))
