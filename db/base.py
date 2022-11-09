from databases import Database
from sqlalchemy import create_engine, MetaData
from core.config import DATABASE_URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from core.config import init_redis_pool
import json

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(
    DATABASE_URL,
)

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


async def set_redis(user_id: str, questions: dict):
    redis_init = await init_redis_pool()
    redis_init.set(str(user_id), json.dumps([questions]), ex=172800)
    return redis_init
