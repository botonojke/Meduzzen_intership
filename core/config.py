import os
from databases import Database
from starlette.config import Config
from configparser import ConfigParser
from dotenv import load_dotenv
import redis.asyncio as redis


load_dotenv()
config = Config(".env")
DATABASE_URL = config('EE_DATABASE_URL', cast=str)
WEB_HOST = config('WEB_HOST', cast=str)
WEB_PORT = config('WEB_PORT', cast=str)
database = Database(DATABASE_URL)
ACCESS_TOKEN_EXPIRE_MINUTES = 60
ALGORITM = "HS256"
KEY = config('KEY', cast=str)
SECRET_KEY = config(
    "EE_SECRET_KEY",
    cast=str,
    default=KEY,
)
REDIS = config("REDIS_URL")

def set_up():
    """Sets up configuration for the app"""

    auth0_config = {
        "DOMAIN": os.getenv("DOMAIN", default="your.domain.com"),
        "API_AUDIENCE": os.getenv("API_AUDIENCE", default="your.audience.com"),
        "ISSUER": os.getenv("ISSUER", default="https://your.domain.com/"),
        "ALGORITHMS": os.getenv("ALGORITHMS", default="RS256"),
    }
    return auth0_config


async def init_redis_pool() -> redis.Redis:
    redis_c = await redis.from_url(
        REDIS,
        encoding="utf-8",
        db=0,
        decode_responses=True,
    )
    return redis_c



# async def init_redis_pool() -> redis.Redis:
#     redis_c = await redis.from_url(
#         'redis://redis',
#         encoding="utf-8",
#         db=0,
#         decode_responses=True,
#     )
#     return redis_c