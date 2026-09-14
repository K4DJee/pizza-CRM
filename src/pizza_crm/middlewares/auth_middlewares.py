from fastapi import Request, HTTPException, status


def require_role(allowed_roles:list[str]):
    async def role_checker(request: Request):
        user_role = request.headers.get("X-User-Role")
        if user_role not in allowed_roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "You haven't permissions for this action")
        return role_checker
    return require_role