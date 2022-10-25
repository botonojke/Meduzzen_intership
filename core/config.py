import os
from databases import Database
from starlette.config import Config
from dotenv import load_dotenv

load_dotenv()
config = Config(".env")
DATABASE_URL = config('EE_DATABASE_URL', cast=str)
WEB_HOST = config('WEB_HOST', cast=str)
WEB_PORT = config('WEB_PORT', cast=str)
database = Database(DATABASE_URL)
