from datetime import timedelta
from dotenv import load_dotenv
from utils.string import string_to_list
import os


load_dotenv()


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=float(os.environ.get('ACCESS_TOKEN_LIFETIME'))  # type: ignore
        ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=float(os.environ.get('REFRESH_TOKEN_LIFETIME'))  # type: ignore
        ),
    "ROTATE_REFRESH_TOKENS": True if os.environ.get(
        'ROTATE_REFRESH_TOKENS'
        ) == '1' else False,
    "BLACKLIST_AFTER_ROTATION": True if os.environ.get(
        'BLACKLIST_AFTER_ROTATION'
        ) == '1' else False,
    "SIGNING_KEY": os.environ.get('SIGNING_KEY'),
}

CORS_ALLOWED_ORIGINS = string_to_list('CORS_ALLOWED_ORIGINS')
