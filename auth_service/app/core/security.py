import bcrypt
import datetime
import jwt
from exceptions import exceptions
from config import config
from models.tokens import Tokens

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def verify_token(token:str, secret_key: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=config.ALGORITHM)
        return payload
    except jwt.exceptions.InvalidTokenError as e:
        print(e)
        raise exceptions.InvalidTokenError("Invalid or expired token")

def create_tokens_pair(user_id: str, role: str)-> Tokens:
    access_delta = datetime.timedelta(minutes=int(config.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_delta = datetime.timedelta(days=int(config.REFRESH_TOKEN_EXPIRE_DAYS))

    access_token = create_token(user_id, role, access_delta, config.JWT_ACCESS_SECRET_KEY)
    refresh_token = create_token(user_id, role, refresh_delta, config.JWT_REFRESH_SECRET_KEY)

   
    return Tokens(AccessToken=access_token, RefreshToken=refresh_token)

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