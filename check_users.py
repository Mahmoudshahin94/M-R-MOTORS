#!/usr/bin/env python
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mrmotors.settings')
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_j0pYvOLI1ksd@ep-flat-mouse-ai17ajbm-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require'

django.setup()

from django.contrib.auth.models import User

print("All users in database:")
print("-" * 50)
for user in User.objects.all():
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Is active: {user.is_active}")
    print(f"Is staff: {user.is_staff}")
    print(f"Is superuser: {user.is_superuser}")
    print("-" * 50)

print(f"\nTotal users: {User.objects.count()}")

# Create the correct admin user
email = 'mrtexasmotors@gmail.com'
username = 'admin'
password = 'Aa123123'

if not User.objects.filter(email=email).exists():
    print(f"\nCreating admin user with email: {email}")
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        first_name='Admin',
        last_name='User'
    )
    print(f"✅ Admin user created successfully!")
    print(f"Email: {email}")
    print(f"Username: {username}")
    print(f"Password: {password}")
else:
    print(f"\n✅ Admin user already exists with email: {email}")
