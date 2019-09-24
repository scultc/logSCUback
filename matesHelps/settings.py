"""
Django settings for matesHelps project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
#_*_ coding:utf-8 _*_
import os
import pymysql

# pymysql.install_as_MySQLdb()
import platform
DEFAULT_CHARSET = 'utf-8'
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+mp8+$w=^j2v^#l)51o+8pg^zu$d#30%amlk2p$f68hod9x5j#'

APPID = 'wxc84b45f5439e7c25'
SECRET = '8b23fb5594a94e3443ec77ffd2cdf185'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'announce',
    'feedback',
    'comment',
    'order',
    'account',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'matesHelps.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'matesHelps.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'matesHelp',
        'USER': 'root',
        'PASSWORD':'tmzqq520..',
        'HOST':'129.28.140.83',
        'port':3306,
        'OPTIONS':{
            'charset':'utf8mb4',
        }
    }
    # 'default':{
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME':'database'
    # }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/matesHelps/'
MEDIA_URL = '/media/matesHelps/'
if platform.system()=='Windows':
    STATIC_ROOT = os.curdir + '/static'
    MEDIA_ROOT = os.curdir + '/media'
else:
    STATIC_ROOT = "/var/matesHelps/static"
    MEDIA_ROOT = "/var/matesHelps/media"



#SESSION
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

SESSION_COOKIE_NAME = 'sessionid'

SESSION_COOKIE_PATH = "/"

SESSION_COOKIE_DOMAIN = None

SESSION_COOKIE_SECURE = False

SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_AGE = 100000000

SESSION_EXPIRE_AT_BROWSER_CLOSE = False

SESSION_SAVE_EVENT_REQUEST = False

CSRF_COOKIE_SECURE = False