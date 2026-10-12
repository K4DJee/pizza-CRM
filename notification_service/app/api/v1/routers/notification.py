from fastapi import APIRouter
from schemes.notification import SendToLetter
from services import email_service

router = APIRouter(tags=['Notification'], prefix='/api/v1/notification')


@router.post("/letter-to-email")
async def send_to_letter(
    data: SendToLetter
):
    response = await email_service.send_letter_to_email(data.subject, data.text, data.user_email)
    return response