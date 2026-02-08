"""
WSGI config for mrmotors project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mrmotors.settings')

# Run migrations on Vercel serverless startup
if os.environ.get('VERCEL'):
    import django
    django.setup()
    
    from django.core.management import call_command
    from django.db import connections
    from django.db.utils import OperationalError
    
    try:
        # Test database connection
        conn = connections['default']
        conn.cursor()
        
        # Run migrations if database is accessible
        print("Running migrations on Vercel startup...")
        call_command('migrate', '--noinput', verbosity=0)
        print("Migrations completed successfully")
    except OperationalError as e:
        print(f"Database not accessible, skipping migrations: {e}")
    except Exception as e:
        print(f"Error running migrations: {e}")

application = get_wsgi_application()

# Vercel expects 'app' variable
app = application
