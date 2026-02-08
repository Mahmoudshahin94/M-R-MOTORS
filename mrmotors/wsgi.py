"""
WSGI config for mrmotors project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mrmotors.settings')

# Run migrations on Vercel serverless startup BEFORE initializing the app
if os.environ.get('VERCEL'):
    print("=" * 50, file=sys.stderr)
    print("VERCEL ENVIRONMENT DETECTED", file=sys.stderr)
    print("=" * 50, file=sys.stderr)
    
    import django
    django.setup()
    
    from django.core.management import call_command
    from django.db import connections
    from django.db.utils import OperationalError
    
    try:
        # Test database connection
        print("Testing database connection...", file=sys.stderr)
        conn = connections['default']
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        print("Database connection successful!", file=sys.stderr)
        
        # Run migrations if database is accessible
        print("Running migrations...", file=sys.stderr)
        call_command('migrate', '--noinput', verbosity=1)
        print("=" * 50, file=sys.stderr)
        print("MIGRATIONS COMPLETED SUCCESSFULLY", file=sys.stderr)
        print("=" * 50, file=sys.stderr)
    except OperationalError as e:
        print(f"ERROR: Database not accessible: {e}", file=sys.stderr)
    except Exception as e:
        print(f"ERROR running migrations: {type(e).__name__}: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)

application = get_wsgi_application()

# Vercel expects 'app' variable
app = application
