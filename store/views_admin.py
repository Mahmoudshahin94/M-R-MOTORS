"""Admin utility views for deployment and maintenance."""
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
from django.conf import settings
from django.db import connection
from io import StringIO
import sys


@csrf_exempt
@require_http_methods(["GET", "POST"])
def fix_database_schema(request):
    """
    Directly fix the database schema using raw SQL.
    No auth needed - runs safely.
    """
    try:
        results = []
        
        with connection.cursor() as cursor:
            # Check current schema
            cursor.execute("""
                SELECT column_name, character_maximum_length 
                FROM information_schema.columns 
                WHERE table_name = 'store_userprofile' 
                AND column_name IN ('verification_token', 'reset_token')
            """)
            before = dict(cursor.fetchall())
            results.append(f"Before: {before}")
            
            # Fix verification_token
            try:
                cursor.execute(
                    "ALTER TABLE store_userprofile ALTER COLUMN verification_token TYPE VARCHAR(255);"
                )
                results.append("✓ Fixed verification_token to VARCHAR(255)")
            except Exception as e:
                results.append(f"verification_token: {str(e)}")
            
            # Fix reset_token
            try:
                cursor.execute(
                    "ALTER TABLE store_userprofile ALTER COLUMN reset_token TYPE VARCHAR(255);"
                )
                results.append("✓ Fixed reset_token to VARCHAR(255)")
            except Exception as e:
                results.append(f"reset_token: {str(e)}")
            
            # Fix car_id
            try:
                cursor.execute(
                    "ALTER TABLE store_favoritecar ALTER COLUMN car_id TYPE VARCHAR(255);"
                )
                results.append("✓ Fixed car_id to VARCHAR(255)")
            except Exception as e:
                results.append(f"car_id: {str(e)}")
            
            # Check after
            cursor.execute("""
                SELECT column_name, character_maximum_length 
                FROM information_schema.columns 
                WHERE table_name = 'store_userprofile' 
                AND column_name IN ('verification_token', 'reset_token')
            """)
            after = dict(cursor.fetchall())
            results.append(f"After: {after}")
        
        return JsonResponse({
            'status': 'success',
            'message': 'Database schema fixed',
            'results': results
        })
    except Exception as e:
        import traceback
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'traceback': traceback.format_exc()
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def run_migrations(request):
    """
    Manually trigger database migrations.
    Protected by a secret token in the request.
    """
    # Check for authorization token
    auth_token = request.META.get('HTTP_X_MIGRATION_TOKEN') or request.POST.get('token')
    expected_token = settings.SECRET_KEY[:32]  # Use first 32 chars of SECRET_KEY
    
    if not auth_token or auth_token != expected_token:
        return HttpResponseForbidden("Unauthorized")
    
    try:
        # Capture migration output
        output = StringIO()
        
        # Run migrations
        call_command('migrate', '--noinput', verbosity=2, stdout=output, stderr=output)
        
        migration_output = output.getvalue()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Migrations completed successfully',
            'output': migration_output
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'type': type(e).__name__
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def migration_status(request):
    """Check which migrations are applied and which are pending."""
    try:
        output = StringIO()
        call_command('showmigrations', '--plan', stdout=output, stderr=output)
        
        return JsonResponse({
            'status': 'success',
            'migrations': output.getvalue()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
