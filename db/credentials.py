import os
from databases import Database
from starlette.config import Config
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()
config = Config(".env")
DATABASE_URL = os.getenv('DATABASE_URL')

database = Database(DATABASE_URL)


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
