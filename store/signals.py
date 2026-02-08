from django.dispatch import receiver
from allauth.socialaccount.signals import pre_social_login, social_account_updated
from allauth.account.signals import user_signed_up
from django.core.files.base import ContentFile
import requests
from io import BytesIO


@receiver(pre_social_login)
def populate_profile_from_social(sender, request, sociallogin, **kwargs):
    """
    Populate user profile with data from social login (Google).
    This runs before the social login is saved.
    """
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


@receiver(user_signed_up)
def save_google_profile_picture(sender, request, user, **kwargs):
    """
    Download and save Google profile picture after user signs up.
    """
    # Get the social account
    social_account = user.socialaccount_set.filter(provider='google').first()
    
    if social_account:
        extra_data = social_account.extra_data
        picture_url = extra_data.get('picture')
        
        if picture_url and hasattr(user, 'profile'):
            try:
                # Download the profile picture
                response = requests.get(picture_url, timeout=10)
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
            except Exception as e:
                # Log the error but don't fail the signup process
                print(f"Failed to download Google profile picture: {e}")


@receiver(social_account_updated)
def update_google_profile_picture(sender, request, sociallogin, **kwargs):
    """
    Update Google profile picture when social account is updated.
    """
    user = sociallogin.user
    
    if sociallogin.account.provider == 'google' and hasattr(user, 'profile'):
        extra_data = sociallogin.account.extra_data
        picture_url = extra_data.get('picture')
        
        if picture_url:
            try:
                # Download the profile picture
                response = requests.get(picture_url, timeout=10)
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
            except Exception as e:
                print(f"Failed to update Google profile picture: {e}")
