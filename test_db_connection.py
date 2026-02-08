#!/usr/bin/env python
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mrmotors.settings')
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_j0pYvOLI1ksd@ep-flat-mouse-ai17ajbm-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require'

django.setup()

from django.contrib.auth.models import User
from django.db import connection

print("Testing database connection...")
print(f"Database engine: {connection.settings_dict['ENGINE']}")
print(f"Database name: {connection.settings_dict['NAME']}")

try:
    # Test connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"✅ Database connection successful! Result: {result}")
    
    # Check if admin user exists
    user_count = User.objects.count()
    print(f"✅ Total users in database: {user_count}")
    
    if User.objects.filter(email='mrtexasmotors@gmail.com').exists():
        user = User.objects.get(email='mrtexasmotors@gmail.com')
        print(f"✅ Admin user found: {user.username} ({user.email})")
        print(f"   Is active: {user.is_active}")
        print(f"   Is staff: {user.is_staff}")
        print(f"   Is superuser: {user.is_superuser}")
    else:
        print("❌ Admin user not found!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
