import secrets
import redis

redis_client = redis.Redis.from_url("redis://localhost:6379:6379", True)

async def gen_otp(user_id: int, exp = 600) -> str:
    redis_key = f"pwd_reset_otp:{user_id}"
    existing_otp = redis_client.get(redis_key)
    if existing_otp is not None:
        raise ValueError("OTP already exists")
    otp = f"{secrets.randbelow(900000) + 100000}"
    await redis_client.setex(redis_key, exp, otp)
    return otp;