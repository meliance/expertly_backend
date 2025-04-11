import os
from pathlib import Path
import dj_database_url

from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = "django-insecure-=#uq^q8(ktnd*1xcz_z0e77qpe5nwj$u%!-+0(4uddo8i_-z44"
SECRET_KEY = os.environ.get("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "False".lower()) == "true"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split()

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "django_filters",
    "api",
    "accounts",
    "documents",
    'scheduling',
    'appointment',
    'payments',
    'chat',
    'notification',
    'feedback',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = "expertly.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "expertly.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'expertly',
        'USER': 'expertly_user',
        'PASSWORD': '1inUeg1d1pAnNGzOofxGwPDETBfVbvAt',
        'HOST': 'dpg-cvrm9l8gjchc73bd3130-a.oregon-postgres.render.com',
        'PORT': '5432',
    }
}


database_url = os.environ.get("DATABASE_URL")
if database_url:
    DATABASES["default"] = dj_database_url.parse(database_url)

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}   

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# settings.py
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


# CHAPA_SECRET_KEY = 'CHASECK_TEST-tUZNyUIl653jrBlgm2lCSV2HiaVdJ3Sf'
# CHAPA_PUBLIC_KEY = 'CHAPUBK_TEST-tAHZRrANW6BhvjgDQ7MWXwKdhp64hOVO'
# CHAPA_API_URL = 'https://api.chapa.co/v1/transaction'
# CHAPA_WEBHOOK_URL = 'http://127.0.0.1:8000/api/payments/webhook/' 

# settings.py
CHAPA_SECRET_KEY = 'CHASECK_TEST-tUZNyUIl653jrBlgm2lCSV2HiaVdJ3Sf'
CHAPA_PUBLIC_KEY = 'CHAPUBK_TEST-tAHZRrANW6BhvjgDQ7MWXwKdhp64hOVO'
CHAPA_API_URL = 'https://api.chapa.co/v1/transaction'
# For local testing without frontend
CHAPA_WEBHOOK_URL = 'http://127.0.0.1:8000/api/payments/webhook/'
CHAPA_RETURN_URL = 'http://127.0.0.1:8000/api/payments/success/' 
CHAPA_FAILURE_URL = 'http://127.0.0.1:8000/api/payments/fail/'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'notifications@mydomain.com'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
