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
@require_http_methods(["GET"])
def check_varchar_fields(request):
    """Check all VARCHAR(100) fields in store tables."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name, column_name, character_maximum_length 
                FROM information_schema.columns 
                WHERE table_schema = 'public'
                AND table_name LIKE 'store_%'
                AND data_type = 'character varying'
                ORDER BY table_name, column_name
            """)
            fields = [
                {
                    'table': row[0],
                    'column': row[1],
                    'max_length': row[2]
                }
                for row in cursor.fetchall()
            ]
            
        return JsonResponse({
            'status': 'success',
            'fields': fields
        })
    except Exception as e:
        import traceback
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'traceback': traceback.format_exc()
        }, status=500)


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
                SELECT table_name, column_name, character_maximum_length 
                FROM information_schema.columns 
                WHERE table_schema = 'public'
                AND table_name LIKE 'store_%'
                AND data_type = 'character varying'
                AND character_maximum_length = 100
            """)
            varchar100_fields = cursor.fetchall()
            results.append(f"VARCHAR(100) fields found: {varchar100_fields}")
            
            # Fix all VARCHAR(100) fields to VARCHAR(255)
            for table, column, length in varchar100_fields:
                try:
                    cursor.execute(
                        f"ALTER TABLE {table} ALTER COLUMN {column} TYPE VARCHAR(255);"
                    )
                    results.append(f"✓ Fixed {table}.{column} to VARCHAR(255)")
                except Exception as e:
                    results.append(f"✗ {table}.{column}: {str(e)}")
            
            # Check for missing is_hidden column and add it
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_schema = 'public'
                AND table_name = 'store_car'
                AND column_name = 'is_hidden'
            """)
            has_hidden = cursor.fetchone()
            
            if not has_hidden:
                try:
                    cursor.execute(
                        "ALTER TABLE store_car ADD COLUMN is_hidden BOOLEAN DEFAULT FALSE NOT NULL;"
                    )
                    results.append("✓ Added is_hidden column to store_car table")
                except Exception as e:
                    results.append(f"✗ Adding is_hidden column: {str(e)}")
            else:
                results.append("✓ is_hidden column already exists")
            
            # Add verification fields to UserProfile
            verification_fields = [
                ('verification_code', 'VARCHAR(6)'),
                ('verification_code_created', 'TIMESTAMP'),
                ('phone_verified', 'BOOLEAN DEFAULT FALSE NOT NULL'),
                ('phone_verification_code', 'VARCHAR(6)'),
                ('phone_verification_code_created', 'TIMESTAMP'),
            ]
            
            for field_name, field_type in verification_fields:
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_schema = 'public'
                    AND table_name = 'store_userprofile'
                    AND column_name = %s
                """, [field_name])
                field_exists = cursor.fetchone()
                
                if not field_exists:
                    try:
                        cursor.execute(
                            f"ALTER TABLE store_userprofile ADD COLUMN {field_name} {field_type};"
                        )
                        results.append(f"✓ Added {field_name} column to store_userprofile table")
                    except Exception as e:
                        results.append(f"✗ Adding {field_name} column: {str(e)}")
                else:
                    results.append(f"✓ {field_name} column already exists")
            
            # Check after
            cursor.execute("""
                SELECT table_name, column_name, character_maximum_length 
                FROM information_schema.columns 
                WHERE table_schema = 'public'
                AND table_name LIKE 'store_%'
                AND data_type = 'character varying'
                AND character_maximum_length = 100
            """)
            remaining = cursor.fetchall()
            results.append(f"Remaining VARCHAR(100) fields: {remaining}")
        
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
