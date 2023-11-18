import os
from dotenv import load_dotenv

load_dotenv()

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('ENGINE'),
        'NAME': os.environ.get('NAME'),
        'USER': os.environ.get('USER', ''),
        'PASSWORD': os.environ.get('PASSWORD', ''),
        'HOST': os.environ.get('HOST', ''),
        'PORT': os.environ.get('PORT', ''),
    }
}
