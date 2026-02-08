"""
Initialize site configuration for django-allauth on startup
"""
import os

def init_site():
    """Initialize the Site object with correct domain"""
    try:
        from django.contrib.sites.models import Site
        from allauth.socialaccount.models import SocialApp
        
        # Update site
        site, created = Site.objects.get_or_create(id=1)
        site.domain = 'm-r-motors.vercel.app'
        site.name = 'M&R Motors'
        site.save()
        
        # Get OAuth credentials from environment
        client_id = os.getenv('GOOGLE_OAUTH_CLIENT_ID', '')
        client_secret = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET', '')
        
        if client_id and client_secret:
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
            
            # Link to site
            google_app.sites.add(site)
            
    except Exception as e:
        # Silently fail during cold start
        pass
