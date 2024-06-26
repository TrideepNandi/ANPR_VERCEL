#!/bin/bash

# Clone the project repository to the specified directory
git clone https://github.com/TrideepNandi/ANPR_VERCEL.git /home/ubuntu/ANPR_VERCEL

# Create a virtual environment and activate it
virtualenv /home/ubuntu/env
source /home/ubuntu/env/bin/activate

# Install Python dependencies
pip install -r /home/ubuntu/ANPR_VERCEL/requirements.txt

# Copy Gunicorn service and socket files
sudo cp /home/ubuntu/ANPR_VERCEL/gunicorn/gunicorn.socket /etc/systemd/system/gunicorn.socket
sudo cp /home/ubuntu/ANPR_VERCEL/gunicorn/gunicorn.service /etc/systemd/system/gunicorn.service

# Copy Nginx configuration
sudo rm -f /etc/nginx/sites-enabled/default
sudo cp /home/ubuntu/ANPR_VERCEL/nginx/nginx.conf /etc/nginx/sites-available/ANPR_VERCEL
sudo ln -s /etc/nginx/sites-available/ANPR_VERCEL /etc/nginx/sites-enabled/
