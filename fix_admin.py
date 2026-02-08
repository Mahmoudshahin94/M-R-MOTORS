#!/usr/bin/env python
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mrmotors.settings')
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_j0pYvOLI1ksd@ep-flat-mouse-ai17ajbm-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require'

django.setup()

from django.contrib.auth.models import User

# Get the admin user
user = User.objects.get(username='admin')

# Update email and password
user.email = 'mrtexasmotors@gmail.com'
user.set_password('Aa123123')
user.is_staff = True
user.is_superuser = True
user.is_active = True
user.save()

print("✅ Admin user updated successfully!")
print(f"Username: {user.username}")
print(f"Email: {user.email}")
print(f"Password: Aa123123")
print(f"Is staff: {user.is_staff}")
print(f"Is superuser: {user.is_superuser}")
