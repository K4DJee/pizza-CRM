from fastapi import Request, HTTPException, status, Header, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..exceptions import exceptions
import jwt
from ..config import config

security = security = HTTPBearer()

def require_role(allowed_roles:list[str]):
    async def role_checker(user_context : dict = Depends(get_current_user_context)):
        if user_context["user_role"] not in allowed_roles:
            raise exceptions.PermissionDenied("You haven't permissions for this action")
        return user_context
    return role_checker
