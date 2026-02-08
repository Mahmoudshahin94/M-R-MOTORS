"""Admin utility views for deployment and maintenance."""
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
from django.conf import settings
from io import StringIO
import sys


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
