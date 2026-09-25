from fastapi import FastAPI, APIRouter, HTTPException, status, Depends, Request, Response, Cookie
from sqlalchemy.orm import Session
from ....services import auth_service
from ....schemas.user import RegisterUserRequest, LoginUserRequest, UserResponse, ChangePasswordOneRequest, ChangePasswordTwoRequest, ChangePasswordThreeRequest
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
        new_user = await auth_service.register_auth_service(db, data)
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
        user, tokens = await auth_service.login_auth_service(db, data)
        # Выдача accessToken и refreshToken
        user_agent = request.headers.get("user-agent", "unknown")

        response.set_cookie(
            key="refresh_token",
            value=tokens.RefreshToken,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=config.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        )
        await auth_service.save_refresh_token_to_db(db, user.id, tokens.RefreshToken, user_agent)


        return {"AccessToken":tokens.AccessToken, "RefreshToken":tokens.RefreshToken, "message":"You have successfully logged in"}

    except ValueError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(e))

@router.post("/refresh")
async def refresh_tokens(request: Request, response: Response, refresh_token: str = Cookie(None),
    db: Session = Depends(get_db)):
    # можно прям получить их куки с ключом refresh_token, как в change-password-3 endpoint
    tokens, user_id = await auth_service.refresh_token_auth_service(db, refresh_token)
    
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

    await auth_service.save_refresh_token_to_db(db, user_id, tokens.RefreshToken, user_agent)

      # 5. Возвращаем новый Access Token
    return{"AccessToken": tokens.AccessToken}
    

@router.post("/change-password-stage-1")
async def change_password_1(
    data: ChangePasswordOneRequest,
    db: Session = Depends(get_db)
):
    response = await auth_service.gen_otp_send_email(db, data.email)   
    if response is True:
        return {"message": "OTP has been succesfully sent in your email"}

@router.post("/change-password-stage-2")
async def change_password_2(
    response: Response,
    data: ChangePasswordTwoRequest,
    db: Session = Depends(get_db)
):
    reset_token = await auth_service.verify_otp_gen_reset_token_auth_service(db, data.email, data.otp)
    response.set_cookie(
        key="reset_token",
        value=reset_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=config.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )

    return {"message": "Succesfully generated a ResetToken"}

@router.post("/change-password-stage-3")
async def change_password_3(
    request: Request,
    data: ChangePasswordThreeRequest,
    db: Session = Depends(get_db)
):
    reset_token = request.cookies.get("reset_token")
    await auth_service.verify_reset_token_change_password_auth_service(db, data.email, reset_token, data.new_password)
    return {"message": "Password succesfully changed!"}

@router.get("/me", response_model=UserResponse)
async def get_profile(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    user = await auth_service.get_userdata(db, token)
    return user # reponse_model сама уберёт лишний пароль 

@router.delete("/me")
async def gelete_profile():
    
    pass