#!/usr/bin/env python
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mrmotors.settings')
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_j0pYvOLI1ksd@ep-flat-mouse-ai17ajbm-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require'

django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

# Get credentials from environment variables
client_id = os.getenv('GOOGLE_OAUTH_CLIENT_ID', '')
client_secret = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET', '')

if not client_id or not client_secret:
    print("❌ Error: GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET must be set")
    exit(1)

# Update the site domain
site = Site.objects.get(id=1)
site.domain = 'm-r-motors.vercel.app'
site.name = 'M&R Motors'
site.save()
print(f"✅ Site updated: {site.domain}")

# Create or update Google OAuth app
google_app, created = SocialApp.objects.get_or_create(
    provider='google',
    defaults={
        'name': 'Google',
        'client_id': client_id,
        'secret': client_secret,
    }
)

if not created:
    google_app.client_id = client_id
    google_app.secret = client_secret
    google_app.save()
    print("✅ Google OAuth app updated")
else:
    print("✅ Google OAuth app created")

# Link the app to the site
google_app.sites.add(site)
print("✅ Google OAuth app linked to site")

print("\n🎉 Google OAuth is now configured!")
print(f"Client ID: {client_id[:20]}...")
