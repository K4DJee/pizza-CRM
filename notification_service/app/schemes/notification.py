from pydantic import BaseModel, Field, EmailStr, UUID4

class SendToLetter(BaseModel):
    subject: str
    text: str
    user_email: str