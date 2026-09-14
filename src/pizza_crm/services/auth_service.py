from sqlalchemy.orm import Session
from ..schemas.user import RegisterUserRequest, LoginUserRequest
from ..db.models.user import User
from sqlalchemy.exc import IntegrityError
import bcrypt
import datetime
import jwt
from ..models.tokens import Tokens
from ..db.models.tokens import Token
from ..config import config
from .redis_service import gen_otp
from .notifications_service import send_letter_to_email



async def register_auth_service(db: Session, data: RegisterUserRequest):
    existing_user = db.query(User).filter(User.mail == data.mail).first()
   
    if existing_user:
        raise ValueError("User with same mail is exists")

    hashed_password = hash_password(data.password)

    new_user = User(
        name=data.name,
        surname = data.surname,
        patronymic = data.patronymic,
        age = data.age,
        mail = data.mail,
        password = hashed_password
    )

    db.add(new_user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("User with same email already exists")

    db.refresh(new_user)
    return new_user

async def login_auth_service(db: Session, data: LoginUserRequest):
    existing_user = db.query(User).filter(User.mail == data.mail).first()
       
    if  not existing_user:
        raise ValueError("Incorrect mail or password")
    print(existing_user)
    if not verify_password(data.password, existing_user.password):
        raise ValueError("Incorrect mail or password")

    return existing_user

    

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password) -> bool:
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def verify_token(token:str, secret_key: str):
    try:
        print(token, secret_key)
        payload = jwt.decode(token, secret_key, algorithms=config.ALGORITHM)
        return payload
    except jwt.exceptions.InvalidTokenError:
        raise ValueError("Invalid or expired token")

def create_tokens_pair(user_id: str)-> Tokens:
    access_delta = datetime.timedelta(minutes=int(config.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_delta = datetime.timedelta(days=int(config.REFRESH_TOKEN_EXPIRE_DAYS))

    access_token = create_token(user_id, access_delta, config.JWT_ACCESS_SECRET_KEY)
    refresh_token = create_token(user_id, refresh_delta, config.JWT_REFRESH_SECRET_KEY)

   
    return Tokens(AccessToken=access_token, RefreshToken=refresh_token)

async def save_refresh_token_to_db(db: Session, user_id: int, refresh_token: str, user_agent:str):
    now = datetime.datetime.now(datetime.timezone.utc)
    expires_at =  now + datetime.timedelta(days=int(config.REFRESH_TOKEN_EXPIRE_DAYS))

    db_token = Token(
        user_id = user_id,
        refresh_token = refresh_token,
        expires_at = expires_at,
        user_agent = user_agent
    )

    db.add(db_token)
    db.commit()


def create_token(
    subject: str,
    expires_delta:datetime.timedelta,
    secret_key:str
) -> str:
    expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    to_encode = {"exp":expire, "sub":subject}
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm= config.ALGORITHM)
    return encoded_jwt

async def get_userdata(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise ValueError("The user don't exist")
    return user

async def gen_otp_send_email(user_id: int, user_email: str):
    try:
        otp = await gen_otp(user_id)
        text = "Insert otp for changing your password"
        await send_letter_to_email(otp, text, user_email)
        return {"message": "OTP has been succesfully sent in your email"}
    except ValueError as e:
        raise ValueError(str(e))