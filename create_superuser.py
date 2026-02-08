#!/usr/bin/env python
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mrmotors.settings')
django.setup()

from django.contrib.auth.models import User

# Create superuser
email = 'mrtexasmotors@gmail.com'
username = 'admin'
password = 'Aa123123'

# Check if user already exists
if User.objects.filter(email=email).exists():
    print(f"User with email {email} already exists!")
    user = User.objects.get(email=email)
    print(f"Username: {user.username}")
else:
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"Superuser created successfully!")
    print(f"Email: {email}")
    print(f"Username: {username}")
    print(f"Password: {password}")
