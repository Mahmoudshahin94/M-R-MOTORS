#!/bin/bash
# Script to run Django migrations on production database

echo "Running database migrations..."
python manage.py migrate

echo ""
echo "Creating superuser..."
python manage.py createsuperuser
