from fastapi_mail import ConnectionConfig, MessageSchema, MessageType, FastMail
from ..config import config

email_config = ConnectionConfig(
    MAIL_USERNAME= config.MAIL_USERNAME,
    MAIL_PASSWORD = config.MAIL_PASSWORD,
    MAIL_FROM =config.MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER =config.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def send_letter_to_email(subject: str, text: str, user_email: str):
    html = f"""
    {text}
    """

    message = MessageSchema(
        subject=subject,
        recipients=user_email,
        body=html,
        subtype=MessageType.html
    )
    try:
        fm = FastMail(email_config)
        await fm.send_message(message)

        return {"message": "OTP has been succesfully sent in your email"}
    except: 
        raise ValueError("OTP has not been sent in your email")
        