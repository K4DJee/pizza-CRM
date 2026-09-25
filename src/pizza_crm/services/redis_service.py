import secrets
import redis.asyncio as redis
import uuid
from ..exceptions import exceptions

redis_port = 6379
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

async def gen_otp(user_id: int, exp = 600) -> str:
    pwd_reset_key = f"pwd_reset_otp:{user_id}"
    existing_otp = await redis_client.get(pwd_reset_key)
    if existing_otp is not None:
        raise exceptions.OTPExists("OTP already exists")
    otp = f"{secrets.randbelow(900000) + 100000}"
    await redis_client.set(pwd_reset_key, otp, ex=exp)
    return otp

async def verify_otp_gen_reset_token(user_id: int, user_otp: str, exp = 600) -> str:
    pwd_reset_key = f"pwd_reset_otp:{user_id}"
    existing_otp = await redis_client.get(pwd_reset_key)
    if existing_otp is None:
        raise exceptions.OTPNotFound("OTP doesn't exists")
    # верификация provided и user_otp
    if existing_otp != user_otp:
        raise exceptions.OTPNotMatch("OTP doesn't match")
    reset_token_key = f"reset_token:{user_id}"
    existing_reset_token = await redis_client.get(reset_token_key)
    if existing_reset_token is not None:
        raise exceptions.ReetTokenExists("ResetToken already exists")
    reset_token = str(uuid.uuid4())
    await redis_client.delete(pwd_reset_key)
    await redis_client.set(reset_token_key, reset_token, exp)

    return reset_token

async def verify_reset_token(user_id: int, reset_token) -> bool:
    reset_token_key = f"reset_token:{user_id}"
    existing_reset_token = await redis_client.get(reset_token_key)
    if existing_reset_token is None:
        raise exceptions.ResetTokenNotFound("ResetToken doesn't exists")
    if existing_reset_token != reset_token:
        raise exceptions.ResetTokenNotMatch("ResetToken not match")
    await redis_client.delete(reset_token_key)
    return True