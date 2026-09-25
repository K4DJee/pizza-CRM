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
from ..schemas.user import ChangePasswordTwoRequest
from . import db_service, redis_service, notifications_service
from ..exceptions import exceptions


async def register_auth_service(db: Session, data: RegisterUserRequest):
    existing_user = await db_service.find_user_by_email(db, data.email)
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

async def login_auth_service(db: Session, data: LoginUserRequest) -> tuple[User, Tokens]:
    existing_user = await db_service.find_user_by_email(db, data.email)
       
    if  not existing_user:
        raise ValueError("Incorrect mail or password")
    print(existing_user)
    if not verify_password(data.password, existing_user.password):
        raise ValueError("Incorrect mail or password")

    tokens = create_tokens_pair(str(existing_user.id), existing_user.role)

    return existing_user, tokens

async def refresh_token_auth_service(db:Session, refresh_token: str) -> tuple[Tokens, int]:
    payload = verify_token(refresh_token, config.JWT_REFRESH_SECRET_KEY)
    user_id = payload.get("sub")
    # проверка на существование пользователя
    user = await db_service.find_user_by_id(db, int(user_id))

    # 3. Генерируем  Access Token и refresh
    tokens = create_tokens_pair(user.id, user.role)

    # 5. Возвращаем новый Access Token
    return tokens, int(user.id)

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
        payload = jwt.decode(token, secret_key, algorithms=config.ALGORITHM)
        return payload
    except jwt.exceptions.InvalidTokenError:
        raise exceptions.InvalidTokenError("Invalid or expired token")

def create_tokens_pair(user_id: str, role: str)-> Tokens:
    access_delta = datetime.timedelta(minutes=int(config.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_delta = datetime.timedelta(days=int(config.REFRESH_TOKEN_EXPIRE_DAYS))

    access_token = create_token(user_id, role, access_delta, config.JWT_ACCESS_SECRET_KEY)
    refresh_token = create_token(user_id, role, refresh_delta, config.JWT_REFRESH_SECRET_KEY)

   
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
    role: str,
    expires_delta:datetime.timedelta,
    secret_key:str
) -> str:
    expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    to_encode = {"exp":expire, "sub":subject, "role": role}
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm= config.ALGORITHM)
    return encoded_jwt

async def get_userdata(db: Session,  token: str):
    payload = verify_token(token, config.JWT_ACCESS_SECRET_KEY)
    user_id = payload.get("sub")
    if user_id is None:
        raise exceptions.InvalidTokenPayload("Invalid token payload")
    user = await db_service.find_user_by_id(db, int(user_id))

    return user

async def gen_otp_send_email(db: Session, user_email: str) -> bool:
    try:
        user = await db_service.find_user_by_email(db, user_email)
        subject = "OTP for changing password"
        otp = await redis_service.gen_otp(user.id)
        text = f"Insert this code {otp} for changing your password"
        await notifications_service.send_letter_to_email(subject, text, user_email)
        return True
    except ValueError:
        raise

async def verify_otp_gen_reset_token_auth_service(
    db: Session,
    email: str, otp: str
) -> str:
    user = await db_service.find_user_by_email(db, email)
    reset_token = await redis_service.verify_otp_gen_reset_token(user.id, otp)
    return reset_token

async def verify_reset_token_change_password_auth_service(
    db: Session,
    email: str, reset_token: str, new_password: str
) -> None:
    user = await db_service.find_user_by_email(db, email)
    isValid = await redis_service.verify_reset_token(user.id, reset_token)
    if isValid is not True:
        raise exceptions.ResetTokenNotMatch("ResetToken don't match")
    new_hashed_password = hash_password(new_password)
    await db_service.update_user_password(db, user.id, new_hashed_password)