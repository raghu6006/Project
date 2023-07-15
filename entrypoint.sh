#!/bin/bash

# Wait for the db service to become healthy
echo "Waiting for the db service to become healthy..."

python wait_for_db.py
python manage.py migrate
echo "The db service is now healthy."

# Run the Django development server
python manage.py runserver 0.0.0.0:80 
#tail -f /dev/null
