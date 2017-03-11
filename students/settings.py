# coding: utf-8
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

"""
Django settings for kg_lang project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xw4j6tj!u$q5&tq#*e-&xttaeca15)q6pg5h-6a8m-*kl@f6%1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', ]

# Application definition

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'polymorphic',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'ckeditor',
    'students',
    'contest',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'students.urls'

AUTH_USER_MODEL = 'students.MyUser'

WSGI_APPLICATION = 'students.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ],
            'debug': DEBUG
        }
    },
]


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

LANGUAGES = [
    ('ru', 'Русский'),
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_L10N = True

USE_TZ = False

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [['Smiley', 'Bold', 'Italic', 'Underline', 'Strike'], ['Link', 'Unlink'], ['Source']],
        'height': 150,
        'width': '100%',
        'toolbarCanCollapse': False,
    },
    'article': {
        'toolbar': [['Smiley', 'Bold', 'Italic', 'Underline', 'Strike'], ['Link', 'Unlink'], ['CodeSnippet', 'Source']],
        'height': 150,
        'width': 800,
        'toolbarCanCollapse': False,
        'extraAllowedContent': '*[*]; table[*]; tr[*]; td[*]; th[*]; h3[*]; h4[*]',
        'extraPlugins': ','.join(
            [
                'codesnippet',
                'widget',
                'dialog',
            ]),
    },
    'short': {
        'toolbar': [['Font', 'FontSize', 'TextColor', 'BGColor'], ['Bold', 'Italic', 'Underline', 'Strike'],
                    ['NumberedList', 'BulletedList'],
                    ['Link', 'Unlink'],
                    ['Smiley', 'Image']],
        'height': 150,
        'toolbarCanCollapse': False,
    },
    'long': {
        'toolbar': [['Font', 'FontSize', 'TextColor', 'BGColor'], ['Bold', 'Italic', 'Underline', 'Strike'],
                    ['NumberedList', 'BulletedList'],
                    ['Link', 'Unlink'],
                    ['Smiley', 'Image']],
        'height': 250,
        'width': '100%',
        'toolbarCanCollapse': False,
    }
}

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'info_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'info.log'),
            'formatter': 'verbose'
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'error.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['error_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")  # from where to collect static files
]
STATIC_ROOT = os.path.join(BASE_DIR,
                           "collected_static")  # to where to store static files. better do it with proxy server

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

try:
    from local_settings import *
except ImportError:
    pass

try:
    from email_settings import *
except ImportError:
    pass
