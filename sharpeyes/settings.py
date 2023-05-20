from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-4pl%ud$^v&=8-x9ms1ku%xzv#b!ys&$1egtvqi^!n4ehz2kjgt'

DEBUG = True

ALLOWED_HOSTS = ['mysite.com', '127.0.0.1']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mainapp.apps.MainappConfig',
    'social_django',
    'calendar',
    'uuslug',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sharpeyes.urls'

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

SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_EMAIL_FORM_URL = '/login-form/'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '948248851315-fligescr1aqrbsiudief96o9kujt8itp.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'
SOCIAL_AUTH_TELEGRAM_BOT_TOKEN = '5777561664:AAEM6PVmJ689eUbSQXtHO4z502u0HDNCc5M'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',       #user attributes(description)
    'social_core.pipeline.social_auth.social_uid',
    #'social_core.pipeline.social_auth.auth_allowed',        #this is where emails and domains whitelists are applied (if defined).
    'social_core.pipeline.social_auth.social_user',          #checking an existing user
    #'social_core.pipeline.user.get_username',
    #'social_core.pipeline.social_auth.associate_by_email',  #social accounts association 
    'mainapp.pipeline.custom_associate_by_email',            #custom social accounts association 
    'mainapp.pipeline.email_preparation',                    #custom pipeline for telegram email field
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    #'social_core.pipeline.user.user_details',
    'mainapp.pipeline.user_details',
)

SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    'social.pipeline.disconnect.allowed_to_disconnect',
    'social.pipeline.disconnect.get_entries',
    'social.pipeline.disconnect.revoke_tokens',
    'social.pipeline.disconnect.disconnect',
    'mainapp.pipeline.stay', 
)

# перенаправление при успешной авторизации
LOGIN_REDIRECT_URL = '/'

WSGI_APPLICATION = 'sharpeyes.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'itversesite@gmail.com'
EMAIL_HOST_PASSWORD = 'xiniufscoqjtdczf'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
#EMAIL_USE_SSL = True
PASSWORD_RESET_TIMEOUT = 7200