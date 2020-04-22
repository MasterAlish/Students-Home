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
    'pipeline',
    'ckeditor',
    'ckeditor_uploader',
    'students',
    'contest',
    'cooler',
    'events',
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
                "students.extension.context.students",
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

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [['Smiley', 'Bold', 'Italic', 'Underline', 'Strike'], ['Link', 'Unlink'], ['Source']],
        'height': 150,
        'width': '100%',
        'toolbarCanCollapse': False,
    },
    'article': {
        'toolbar': [['Format', 'Font', 'FontSize'], ['Smiley', 'Bold', 'Italic', 'Underline', 'Strike'],
                    ['TextColor', 'BGColor'],  ['Link', 'Unlink', 'Anchor'], ['CodeSnippet', 'Source'],
                    ['Image', 'Table']],
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
                    ['CodeSnippet'],
                    ['Smiley', 'Image']],
        'height': 250,
        'width': '100%',
        'toolbarCanCollapse': False,
        'extraPlugins': ','.join(
            [
                'codesnippet',
                'widget',
                'dialog',
            ]),
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
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "cooler", "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "collected_static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

PIPELINE = {
    'STYLESHEETS': {
        'students': {
            'source_filenames': (
                'css/students/students1.css',
                'css/students/font-awesome.css',
                'bootstrap/css/bootstrap.css',
                'css/bootstrap-datepicker3.min.css'
            ),
            'output_filename': 'css/students.css',
            'variant': 'datauri',
            'extra_context': {
                'media': 'screen,projection',
            },
        },
    },
    'JAVASCRIPT': {
        'students': {
            'source_filenames': (
              'js/students/jquery-2.1.1.js',
              'js/students/utils.js',
              'bootstrap/js/bootstrap.js',
              'js/bootstrap-datepicker.min.js',
              'js/bootstrap-datepicker.ru.min.js',
            ),
            'output_filename': 'js/students.js',
        }
    },
    'JS_COMPRESSOR': 'pipeline.compressors.jsmin.JSMinCompressor',
    'CSS_COMPRESSOR': 'pipeline.compressors.cssmin.CSSMinCompressor',
}

try:
    from local_settings import *
except ImportError:
    pass

try:
    from email_settings import *
except ImportError:
    pass
