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

async def get_current_user_context(credentials: HTTPAuthorizationCredentials = Depends(security)): # 3 точки обозначают, что это обязательный параметр
    token = credentials.credentials

    try:
        payload = jwt.decode(token, config.JWT_ACCESS_SECRET_KEY, algorithms=[config.ALGORITHM])
        user_id = payload.get("sub")
        user_role = payload.get("role")
        if not user_id or not user_role:
            raise exceptions.InvalidTokenPayload("Invalid token payload")

        return {"user_id": int(user_id), "user_role": user_role}
        
    except jwt.ExpiredSignatureError and jwt.InvalidTokenError:
        raise exceptions.InvalidTokenError("Invalid or expired token")