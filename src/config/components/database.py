import os

from config.components.boilerplate import BASE_DIR

from dotenv import load_dotenv

load_dotenv()


if int((os.environ.get("DEBUG"))):
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB"),
            "USER": os.environ.get("POSTGRES_USER"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
            "HOST": "db",
            "PORT": 5432,
        }
    }

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'