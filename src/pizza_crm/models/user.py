from pydantic import BaseModel, Field


class RegisterUser(BaseModel):
    name: str
    surname: str
    patronymic: str
    age: int
    mail: str

