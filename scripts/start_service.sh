#!/usr/bin/env bash

# Start Gunicorn service
sudo systemctl start gunicorn.service
sudo systemctl enable gunicorn.service

# Add user to www-data group
sudo gpasswd -a www-data ubuntu

# Start Django server
python /home/ubuntu/ANPR_VERCEL/manage.py runserver 0.0.0.0:8000

# Restart Nginx
sudo systemctl restart nginx