FROM django:python2-onbuild

ONBUILD RUN apt-get install -y  libtiff5-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev


ONBUILD CMD ["python", "./manage.py", "makemigrations", "--no-input"]
ONBUILD CMD ["python", "./manage.py", "migrate", "--no-input"]
ONBUILD CMD ["python", "./manage.py", "collectstatic", "--no-input"]
