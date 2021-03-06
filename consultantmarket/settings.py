"""
Django settings for consultantmarket project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
'''
Important configuration

If you are working localy with docker
you need to set the Debug variable to True and add to the dictonary DATABASES the next kay-value pair
'HOST': 'mongo'
and modify the document properties.txt, it has more instructions.

If you are working from a server
you need to set the Debug variable to False and remove from the dictonary DATABASES the next kay-value pair
'HOST': 'mongo'
and modify the document properties.txt, it has more instructions.

Remember: We are using the next command to run the app in server
python3 manage.py runserver --insecure
'''
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o&nx!s$tilel2kn7^$1%4vdo*g5zpu9+e4d8*668w(oj!99jde'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# When this flag is set to true, fake data is used
FAKE_DATA = False

ALLOWED_HOSTS = ["40.113.199.40","localhost","127.0.0.1","https://skillssearcher.intersysconsulting.com/","django"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bios',
    'ntlm',
    'office365',
    'search',
    'roster'
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

ROOT_URLCONF = 'consultantmarket.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'consultantmarket.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'consultantmarket',
        'HOST': 'mongo',
        'ENFORCE_SCHEMA': False
        }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "consultantmarket/static"),
]

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

# Bios settings

BIOS_ROOT = os.path.join(MEDIA_ROOT, 'resumes')

SHAREPOINT_URL = 'https://intersysconsulting.sharepoint.com/'

BIOS_URL = (
    '{}mexico/Shared%20Documents/Forms/AllItems.aspx?'
    'RootFolder=%2Fmexico%2FShared%20Documents%2FResumes'.format(
        SHAREPOINT_URL
    )
)

SHAREPOINT_PREFIX = (
    'mexico/Shared Documents/Forms/AllItems.aspx?'
    'Paged=TRUE&p_SortBehavior=0&p_FileLeafRef='
)

SHAREPOINT_SUFFIX = (
    '&p_ID=815&RootFolder=%2fmexico%2fShared%20Documents%2fResumes&'
    'PageFirstRow=31&View=d8edd401-9206-4309-8d07-a5c43cfc3180'
)
try:
    from .localsettings import *
except:
    pass

EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_HOST_USER = 'intersysinternalapp@intersysconsulting.com'
EMAIL_HOST_PASSWORD = 'Internal2018!'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
