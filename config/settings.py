import os
import secrets
from split_settings.tools import include

from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = str(os.environ.get("SECRET_KEY") or secrets.token_hex(32))

DEBUG = bool(os.environ.get("DEBUG", False))

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(',')

config_folder = "components/"

config_files = [
    "apps.py",
    "auth.py",
    "boilerplate.py",
    "database.py",
    "internationalization.py",
    "middleware.py",
    "static.py",
    "templates.py",
    "timezone.py",
]

include(*(config_folder + file for file in config_files))







