from pydantic import BaseModel, Field, EmailStr, UUID4
import datetime

class RegisterUserRequest(BaseModel):
    name: str
    surname: str
    patronymic: str
    age: int
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

class LoginUserRequest(BaseModel):
    email: EmailStr 
    password: str = Field(min_length=8, max_length=72)

class UserResponse(BaseModel):
    name: str
    surname: str
    patronymic: str
    age: int
    mail: EmailStr
    updatedAt: datetime.datetime # поменять на _
    createdAt: datetime.datetime

class ChangePasswordOneRequest(BaseModel):
    email: EmailStr

class ChangePasswordTwoRequest(BaseModel):
    email: EmailStr
    otp: str = Field(min_length=6, max_length=6)

class ChangePasswordThreeRequest(BaseModel):
    email: EmailStr
    new_password: str = Field(min_length=8, max_length=72)
    