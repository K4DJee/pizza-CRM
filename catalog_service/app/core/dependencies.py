from fastapi import Request, HTTPException, status, Header, Depends
from fastapi.responses import JSONResponse
from httpx import RequestError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.user import UserContext
from exceptions import exceptions
import jwt
from config import config
from httpclient import http_client

security = security = HTTPBearer()

def require_role(allowed_roles:list[str]):
    async def role_checker(user_context : UserContext = Depends(get_current_user_context)):
        if user_context.role not in allowed_roles:
            raise exceptions.PermissionDenied("You haven't permissions for this action")
        return user_context
    return role_checker

async def get_current_user_context(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserContext | None:
    token = credentials.credentials

    try:
        response = await http_client.get( 
            url=f"{config.AUTH_SERVICE_URL}/api/v1/auth/me", 
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        try:
            content: UserContext= response.json()
        except Exception:
            content = {"detail": response.text}

        client_response = JSONResponse(
            status_code=response.status_code,
            content=content
        )

        if client_response.status_code >= 400:
            return client_response

        return content

    except RequestError as e:
        raise exceptions.RequestError(f"Auth Service недоступен: {str(e)}")
    except Exception as e:
        print(e)
        raise exceptions.InternalServerError("Internal Server Error")
