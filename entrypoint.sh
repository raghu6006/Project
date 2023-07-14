#!/bin/bash

# Wait for MySQL to start
#while ! nc -z localhost 3306; do
#  sleep 1
#done

# Run database migrations
#python manage.py makemigrations process
python manage.py migrate

# Run the Django development server
python manage.py runserver 0.0.0.0:80

