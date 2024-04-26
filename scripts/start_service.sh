#!/usr/bin/env bash

# Start Gunicorn service
sudo systemctl start gunicorn.service
sudo systemctl enable gunicorn.service

# Start Django server
python3 /home/ubuntu/ANPR_VERCEL/manage.py runserver 0.0.0.0:8000

# Restart Nginx
sudo systemctl restart nginx