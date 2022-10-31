import os
from databases import Database
from starlette.config import Config
from configparser import ConfigParser
# from dotenv import load_dotenv
#
# load_dotenv()
config = Config(".env")
DATABASE_URL = config('EE_DATABASE_URL', cast=str)
WEB_HOST = config('WEB_HOST', cast=str)
WEB_PORT = config('WEB_PORT', cast=str)
database = Database(DATABASE_URL)
ACCESS_TOKEN_EXPIRE_MINUTES = 60
ALGORITM = "HS256"
SECRET_KEY = config(
    "EE_SECRET_KEY",
    cast=str,
    default='baafdde3fc693d8be0045ae82c6d8fcfc343e909f6c17169811d023e3ba26964',
)

def set_up():
    """Sets up configuration for the app"""




    auth0_config = {
        "DOMAIN": os.getenv("DOMAIN", default="your.domain.com"),
        "API_AUDIENCE": os.getenv("API_AUDIENCE", default="your.audience.com"),
        "ISSUER": os.getenv("ISSUER", default="https://your.domain.com/"),
        "ALGORITHMS": os.getenv("ALGORITHMS", default="RS256"),
    }
    return auth0_config
