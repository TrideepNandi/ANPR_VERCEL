#!/bin/bash

# Perform any additional operations specific to your application here
# For example, you might want to run database migrations, collect static files, etc.

# Activate the virtual environment
source /home/ubuntu/env/bin/activate

# Run Django migrations
python3 /home/ubuntu/ANPR_VERCEL/manage.py migrate
python3 /home/ubuntu/ANPR_VERCEL/manage.py migrate

# Collect static files
python3 /home/ubuntu/ANPR_VERCEL/manage.py collectstatic --noinput
