#!/usr/bin/env bash

# Django operations
sed -i 's/\[]/\["54.144.250.113"]/' /home/ubuntu/ANPR_VERCEL/ANPR_VERCEL/settings.py
python manage.py migrate
python manage.py makemigrations
python manage.py collectstatic

# Restart services
sudo service gunicorn restart
sudo service nginx restart