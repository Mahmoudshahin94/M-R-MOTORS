from django.dispatch import receiver
from allauth.socialaccount.signals import pre_social_login, social_account_updated
from allauth.account.signals import user_signed_up
from django.core.files.base import ContentFile
from django.conf import settings
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Optional: Only import requests if available (for development/debugging)
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logger.warning("requests library not available - profile picture sync disabled")


@receiver(pre_social_login)
def populate_profile_from_social(sender, request, sociallogin, **kwargs):
    """
    Populate user profile with data from social login (Google).
    This runs before the social login is saved.
    """
    try:
        user = sociallogin.user
        
        # If this is a new user (not yet saved to database)
        if not user.pk:
            # Get extra data from social account
            if sociallogin.account.provider == 'google':
                extra_data = sociallogin.account.extra_data
                
                # Set user's name from Google account
                if not user.first_name and extra_data.get('given_name'):
                    user.first_name = extra_data.get('given_name', '')
                if not user.last_name and extra_data.get('family_name'):
                    user.last_name = extra_data.get('family_name', '')
    except Exception as e:
        logger.error(f"Error populating profile from social login: {e}")
        # Don't raise - allow login to continue


@receiver(user_signed_up)
def save_google_profile_picture(sender, request, user, **kwargs):
    """
    Download and save Google profile picture after user signs up.
    Only runs if requests library is available.
    """
    # Skip if requests not available (serverless environment)
    if not REQUESTS_AVAILABLE:
        return
    
    try:
        # Get the social account
        social_account = user.socialaccount_set.filter(provider='google').first()
        
        if social_account:
            extra_data = social_account.extra_data
            picture_url = extra_data.get('picture')
            
            if picture_url and hasattr(user, 'profile'):
                try:
                    # Download the profile picture with short timeout
                    response = requests.get(picture_url, timeout=5)
                    if response.status_code == 200:
                        # Get file extension from URL or default to jpg
                        file_ext = 'jpg'
                        if '.' in picture_url:
                            file_ext = picture_url.split('.')[-1].split('?')[0]
                        
                        # Create a file name
                        file_name = f'google_profile_{user.id}.{file_ext}'
                        
                        # Save the image to the profile
                        user.profile.profile_picture.save(
                            file_name,
                            ContentFile(response.content),
                            save=True
                        )
                        logger.info(f"Saved Google profile picture for user {user.id}")
                except requests.RequestException as e:
                    logger.warning(f"Failed to download Google profile picture: {e}")
                except Exception as e:
                    logger.error(f"Error saving Google profile picture: {e}")
    except Exception as e:
        logger.error(f"Error in save_google_profile_picture signal: {e}")
        # Don't raise - allow signup to continue


@receiver(social_account_updated)
def update_google_profile_picture(sender, request, sociallogin, **kwargs):
    """
    Update Google profile picture when social account is updated.
    Only runs if requests library is available.
    """
    # Skip if requests not available (serverless environment)
    if not REQUESTS_AVAILABLE:
        return
    
    try:
        user = sociallogin.user
        
        if sociallogin.account.provider == 'google' and hasattr(user, 'profile'):
            extra_data = sociallogin.account.extra_data
            picture_url = extra_data.get('picture')
            
            if picture_url:
                try:
                    # Download the profile picture with short timeout
                    response = requests.get(picture_url, timeout=5)
                    if response.status_code == 200:
                        # Get file extension
                        file_ext = 'jpg'
                        if '.' in picture_url:
                            file_ext = picture_url.split('.')[-1].split('?')[0]
                        
                        file_name = f'google_profile_{user.id}.{file_ext}'
                        
                        # Delete old picture if exists
                        if user.profile.profile_picture:
                            user.profile.profile_picture.delete(save=False)
                        
                        # Save the new image
                        user.profile.profile_picture.save(
                            file_name,
                            ContentFile(response.content),
                            save=True
                        )
                        logger.info(f"Updated Google profile picture for user {user.id}")
                except requests.RequestException as e:
                    logger.warning(f"Failed to update Google profile picture: {e}")
                except Exception as e:
                    logger.error(f"Error updating Google profile picture: {e}")
    except Exception as e:
        logger.error(f"Error in update_google_profile_picture signal: {e}")
        # Don't raise - allow update to continue
