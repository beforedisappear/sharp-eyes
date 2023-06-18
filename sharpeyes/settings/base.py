import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'django-insecure-4pl%ud$^v&=8-x9ms1ku%xzv#b!ys&$1egtvqi^!n4ehz2kjgt'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mainapp.apps.MainappConfig',
    'split_settings',
    'social_django',
    'django_hosts',
    'calendar',
    'uuslug',
]

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sharpeyes.urls'
ROOT_HOSTCONF = 'sharpeyes.hosts'
DEFAULT_HOST = " "

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'mainapp.context_processors.get_forms',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (    
    'django.contrib.auth.backends.ModelBackend',    # бекенд классической аутентификации
    'social_core.backends.google.GoogleOAuth2',     # бекенд авторизации через google
    'social_core.backends.telegram.TelegramAuth',   # бекенд авторизации через telegram
)


# перенаправление при успешной авторизации
LOGIN_REDIRECT_URL = '/'

WSGI_APPLICATION = 'sharpeyes.wsgi.application'

AUTH_USER_MODEL = 'mainapp.MyUser'


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# префикс url адреса для статических файлов
STATIC_URL = '/static/'
# путь к общей статической папке web сервера
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# список нестандартных путей к статическим файлам
STATICFILES_DIRS = []

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# формирование пути к каталогу media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# префикс url адреса для медиа  файлов
MEDIA_URL = '/media/'