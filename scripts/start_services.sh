#!/bin/bash

# Start Gunicorn service
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

# Restart Nginx service
sudo systemctl restart nginx

# Run Django development server
source /home/ubuntu/env/bin/activate
python3 /home/ubuntu/ANPR_VERCEL/manage.py runserver 0.0.0.0:8000
