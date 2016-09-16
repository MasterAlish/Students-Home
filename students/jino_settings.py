import os

STATIC_ROOT = os.path.join(os.path.expanduser('~'), 'domains/students.zapto.org/static/')
MEDIA_ROOT = os.path.join(os.path.expanduser('~'), 'domains/students.zapto.org/media/')

DEBUG = False

ALLOWED_HOSTS = ['*',]
