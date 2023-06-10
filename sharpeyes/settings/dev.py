from .base import *
from .social_settings import *
from .email_settings import *
import os

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

ALLOWED_HOSTS = ['mysite.com', '127.0.0.1']