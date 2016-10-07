#!/bin/bash

zip -r update.zip students/ static/ templates/ image/ manage.py requirements.txt send_mails.sh
scp update.zip masteralish@masteralish.myjino.ru:django/students/
rm update.zip
ssh masteralish@masteralish.myjino.ru << END
    cd django/students
    unzip -uo update.zip
    rm update.zip
    if [ -f students/local_settings.py ]; then
        rm students/local_settings.py
    fi
    mv students/jino_settings.py students/local_settings.py

    cd ../../domains/students.zapto.org/
    if [ -f .htaccess ]; then
        rm .htaccess
    fi
    if [ -f jino.wsgi ]; then
        rm jino.wsgi
    fi
    cp ../../django/students/students/jino.wsgi ./
    cp ../../django/students/students/.htaccess ./

    cd ../../django/students/
    source env/bin/activate
    pip install -r req.txt
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput
END
