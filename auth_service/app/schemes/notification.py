from pydantic import BaseModel

class SendToLetter(BaseModel):
    subject: str
    text: str
    user_email: str