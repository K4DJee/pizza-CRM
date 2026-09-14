from pydantic import BaseModel, Field
import datetime

class RegisterUserRequest(BaseModel):
    name: str
    surname: str
    patronymic: str
    age: int
    mail: str
    password: str = Field(min_length=8, max_length=72)

class LoginUserRequest(BaseModel):
    mail: str 
    password: str = Field(min_length=8, max_length=72)

class UserResponse(BaseModel):
    name: str
    surname: str
    patronymic: str
    age: int
    mail: str
    updatedAt: datetime.datetime # поменять на _
    createdAt: datetime.datetime