from fastapi import FastAPI, APIRouter, HTTPException, status, Depends, Request, Response, Cookie, Body
from sqlalchemy.orm import Session
from services import users_service
from schemas.users import RegisterUserRequest, LoginUserRequest, UserResponse, ChangePasswordOneRequest, ChangePasswordTwoRequest, ChangePasswordThreeRequest
from db.session import get_db  
from config import config
from exceptions import exceptions
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(tags=['Authentication'], prefix='/api/v1/auth')

security = HTTPBearer()


@router.post("/register")
async def register(
    data: RegisterUserRequest,
    db: Session = Depends(get_db)
):
    try:
        new_user = await users_service.register_auth_service(db, data)
        return {"message": "User registered", "user_id": new_user.id}
    except ValueError as e:
        raise exceptions.UserNotFoundError(str(e))

@router.post("/login")
async def login(
    data: LoginUserRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    try:
        user, tokens = await users_service.login_auth_service(db, data)
        # Выдача accessToken и refreshToken
        user_agent = request.headers.get("user-agent", "unknown")

        await users_service.save_refresh_token_to_db(db, user.id, tokens.RefreshToken, user_agent)


        return {"AccessToken":tokens.AccessToken, "RefreshToken":tokens.RefreshToken, "message":"You have successfully logged in"}

    except ValueError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(e))

@router.post("/refresh")
async def refresh_tokens(request: Request, refresh_token: str = Body(embed=True),
    db: Session = Depends(get_db)):
    # можно прям получить их куки с ключом refresh_token, как в change-password-3 endpoint
    tokens, user_id = await users_service.refresh_token_auth_service(db, refresh_token)
    
    user_agent = request.headers.get("user-agent", "unknown")

    await users_service.save_refresh_token_to_db(db, user_id, tokens.RefreshToken, user_agent)

      # 5. Возвращаем новый Access Token
    return{"AccessToken": tokens.AccessToken, "RefreshToken": tokens.RefreshToken}
    

@router.post("/change-password-stage-1")
async def change_password_1(
    data: ChangePasswordOneRequest,
    db: Session = Depends(get_db)
):
    response = await users_service.gen_otp_send_email(db, data.email)   
    if response is True:
        return {"message": "OTP has been succesfully sent in your email"}

@router.post("/change-password-stage-2")
async def change_password_2(
    response: Response,
    data: ChangePasswordTwoRequest,
    db: Session = Depends(get_db)
):
    reset_token = await users_service.verify_otp_gen_reset_token_auth_service(db, data.email, data.otp)
    # response.set_cookie(
    #     key="reset_token",
    #     value=reset_token,
    #     httponly=True,
    #     secure=False,
    #     samesite="lax",
    #     max_age=config.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    # )

    return {
        "ResetToken": reset_token,
        "message": "Succesfully generated a ResetToken"
    }

@router.post("/change-password-stage-3")
async def change_password_3(
    request: Request,
    data: ChangePasswordThreeRequest,
    db: Session = Depends(get_db)
):
    reset_token = request.cookies.get("reset_token")
    await users_service.verify_reset_token_change_password_auth_service(db, data.email, reset_token, data.new_password)
    return {"message": "Password succesfully changed!"}

@router.get("/me", response_model=UserResponse)
async def get_profile(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    user = await users_service.get_userdata_auth_service(db, token)
    return user # reponse_model сама уберёт лишний пароль 

@router.delete("/me")
async def delete_profile(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    await users_service.delete_user_profile_auth_service(db, token)
    return {"message": "Your profile was deleted"}


