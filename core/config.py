import os
from databases import Database
from starlette.config import Config
from dotenv import load_dotenv

load_dotenv()
config = Config(".env")
DATABASE_URL = config('EE_DATABASE_URL', cast=str)
database = Database(DATABASE_URL)
