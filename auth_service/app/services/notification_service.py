from fastapi import APIRouter, Response, Cookie, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from exceptions import exceptions
from schemes import notification
from httpclient import http_client
from httpx import RequestError
from config import config


async def proxy_letter_to_email(
    data: notification.SendToLetter
):
    try:
        response = await http_client.post(
            url=f"{config.NOTIFICATION_SERVICE_URL}/api/v1/notification/letter-to-email", 
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
        raise exceptions.RequestError(f"Notification Service недоступен: {str(e)}")