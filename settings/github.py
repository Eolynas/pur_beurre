from . import *

SECRET_KEY = 'c-`3zpC@9gssqJj{W8z|BL\rH'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
