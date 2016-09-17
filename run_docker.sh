#!/usr/bin/env bash

# should be okay
docker ps -a


echo "====================================="
echo "   Trying to delete old django app   "
echo "====================================="
docker stop django-app
docker rm django-app

# build it
echo "====================================="
echo "        building application         "
echo "====================================="
docker build -t students-django-app .


# run and with exposed 8000 port
echo "====================================="
echo "            building done            "
echo "        starting application         "
echo "====================================="
docker run --name django-app -p 8000:8000 -d students-django-app


echo "========================================"
echo "go ahead and open http://localhost:8000"
echo "========================================"
