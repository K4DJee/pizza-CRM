from fastapi import APIRouter, Response, Cookie, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from httpclient import http_client
from exceptions import exceptions
from httpx import RequestError
from schemas import auth
from config import config

router = APIRouter(tags=['Authentication'], prefix='/api/v1/auth')
security = HTTPBearer()

# @router.post
@router.post("/register")
async def proxy_register(
    data:auth.RegisterUserRequest,
):
    try:
        response = await http_client.post(
            url=f"{config.AUTH_SERVICE_URL}/api/v1/auth/register", 
            json=data.model_dump() 
        )

        try:
            content = response.json()
        except Exception:
            content = {"detail": response.text}

        return JSONResponse(
            status_code=response.status_code,
            content=content
        )
    except RequestError as e:
        raise exceptions.RequestError(f"Auth Service недоступен: {str(e)}")

@router.post("/login")
async def proxy_login(
    data: auth.LoginUserRequest,
    response: Response
    ):
    try:
        response = await http_client.post(
            url=f"{config.AUTH_SERVICE_URL}/api/v1/auth/login", 
            json=data.model_dump() 
        )

        try:
            content = response.json()
        except Exception:
            content = {"detail": response.text}

        client_response = JSONResponse(
            status_code=response.status_code,
            content=content
        )

        if client_response.status_code >= 400:
            if client_response.status_code == 401:
                client_response.delete_cookie(key="refresh_token")
            return client_response
        
        client_response.set_cookie(
            key="refresh_token",
            value=content["RefreshToken"],
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=config.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        )    

        return client_response

    except RequestError as e:
        raise exceptions.RequestError(f"Auth Service недоступен: {str(e)}")

@router.post("/refresh")
async def proxy_refresh_token(
    response: Response, 
    refresh_token: str | None = Cookie(default=None)
    ):
    if not refresh_token:
            return JSONResponse(
            status_code=401,
            content={"detail": "Refresh token cookie is missing"},
    )
    try:
        response = await http_client.post(
            url=f"{config.AUTH_SERVICE_URL}/api/v1/auth/refresh", 
            json={"refresh_token": refresh_token}
        )

        try:
            content = response.json()
        except Exception:
            content = {"detail": response.text}
        print(content)
        client_response = JSONResponse(
            status_code=response.status_code,
            content=content
        )

        if client_response.status_code >= 400:
            return client_response
        
        client_response.set_cookie(
            key="refresh_token",
            value=content.get("RefreshToken"),
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=config.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        )

        return client_response

    except RequestError as e:
        raise exceptions.RequestError(f"Auth Service недоступен: {str(e)}")

# @router.post("/change-password-stage-1")
# async def proxy_change_password_1(
#     response: Response, 
#     data: auth.ChangePasswordOneRequest
# ):
#     try:
#         internal_response = await http_client.post(
#             url=f"{config.AUTH_SERVICE_URL}/api/v1/auth/change-password-stage-1", 
#             json=data.model_dump() 
#         )

#         response.set_cookie(
#             key="refresh_token",
#             value=internal_response.get["RefreshToken"],
#             httponly=True,
#             secure=False,
#             samesite="lax",
#             max_age=config.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
#         )

#         try:
#             content = response.json()
#         except Exception:
#             content = {"detail": response.text}

#         return JSONResponse(
#             status_code=response.status_code,
#             content=content
#         )

#     except RequestError as e:
#         raise exceptions.RequestError(f"Auth Service недоступен: {str(e)}")

# @router.post("/change-password-stage-2")
# async def proxy_change_password_2(
#     response: Response,
#     data: auth.ChangePasswordTwoRequest,
# ):
#     try:
#         response = await http_client.post(
#             url=f"{config.AUTH_SERVICE_URL}/api/v1/auth/change-password-stage-2", 
#             json=data.model_dump() 
#         )

#         response.set_cookie(
#             key="refresh_token",
#             value=response["AccessToken"],
#             httponly=True,
#             secure=False,
#             samesite="lax",
#             max_age=config.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
#         )

#         try:
#             content = response.json()
#         except Exception:
#             content = {"detail": response.text}

#         return JSONResponse(
#             status_code=response.status_code,
#             content=content
#         )

#     except RequestError as e:
#         raise exceptions.RequestError(f"Auth Service недоступен: {str(e)}")

# @router.post("/change-password-stage-3")
# async def proxy_change_password_3(
#     request: Request,
#     data: auth.ChangePasswordThreeRequest,
# ):
#     try:
#         response = await http_client.post(
#             url=f"{config.AUTH_SERVICE_URL}/api/v1/auth/change-password-stage-3", 
#             json=data.model_dump() 
#         )

#         response.set_cookie(
#             key="refresh_token",
#             value=response["AccessToken"],
#             httponly=True,
#             secure=False,
#             samesite="lax",
#             max_age=config.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
#         )

#         try:
#             content = response.json()
#         except Exception:
#             content = {"detail": response.text}

#         return JSONResponse(
#             status_code=response.status_code,
#             content=content
#         )

#     except RequestError as e:
#         raise exceptions.RequestError(f"Auth Service недоступен: {str(e)}")

# @router.get("/me", response_model=auth.UserResponse)
# async def proxy_get_profile(
#     credentials: HTTPAuthorizationCredentials = Depends(security),
# ):
#     try:
#         token = credentials.credentials
#         response = await http_client.get(
#             url=f"{config.AUTH_SERVICE_URL}/api/v1/auth/me", 
#             json=token 
#         )

#         response.set_cookie(
#             key="refresh_token",
#             value=response["AccessToken"],
#             httponly=True,
#             secure=False,
#             samesite="lax",
#             max_age=config.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
#         )

#         try:
#             content = response.json()
#         except Exception:
#             content = {"detail": response.text}

#         return JSONResponse(
#             status_code=response.status_code,
#             content=content
#         )

#     except RequestError as e:
#         raise exceptions.RequestError(f"Auth Service недоступен: {str(e)}")

# @router.delete("/me")
# async def proxy_delete_profile(
#     credentials: HTTPAuthorizationCredentials = Depends(security),
# ):
#     try:
#         token = credentials.credentials
#         response = await http_client.delete(
#             url=f"{config.AUTH_SERVICE_URL}/api/v1/auth/me", 
#             json=token
#         )

#         response.set_cookie(
#             key="refresh_token",
#             value=response["AccessToken"],
#             httponly=True,
#             secure=False,
#             samesite="lax",
#             max_age=config.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
#         )

#         try:
#             content = response.json()
#         except Exception:
#             content = {"detail": response.text}

#         return JSONResponse(
#             status_code=response.status_code,
#             content=content
#         )

#     except RequestError as e:
#         raise exceptions.RequestError(f"Auth Service недоступен: {str(e)}")
