from pydantic import BaseModel
import datetime

class UserContext(BaseModel):
    name: str
    surname: str
    patronymic: str
    role: str
    age: int
    mail: str
    updatedAt: datetime.datetime
    createdAt: datetime.datetime