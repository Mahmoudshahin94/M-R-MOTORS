from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom social account adapter to handle email verification for Google OAuth.
    """
    
    def pre_social_login(self, request, sociallogin):
        """
        Called just after a user successfully authenticates via a social provider,
        but before the login is actually processed.
        """
        # If user is signing up (not connecting to existing account)
        if sociallogin.is_existing:
            return
        
        # If email is provided by the social account
        if 'email' in sociallogin.account.extra_data:
            email = sociallogin.account.extra_data['email']
            
            # Mark the email as verified since it comes from Google
            try:
                # Check if email already exists
                email_address = EmailAddress.objects.filter(email=email).first()
                if email_address:
                    # Email exists, mark as verified
                    email_address.verified = True
                    email_address.primary = True
                    email_address.save()
            except Exception:
                pass
    
    def save_user(self, request, sociallogin, form=None):
        """
        Save the user and mark their email as verified.
        """
        user = super().save_user(request, sociallogin, form)
        
        # Mark email as verified for Google accounts
        if sociallogin.account.provider == 'google':
            email = sociallogin.account.extra_data.get('email')
            if email:
                # Get or create EmailAddress and mark as verified
                email_address, created = EmailAddress.objects.get_or_create(
                    user=user,
                    email=email.lower(),
                    defaults={'verified': True, 'primary': True}
                )
                if not created and not email_address.verified:
                    email_address.verified = True
                    email_address.primary = True
                    email_address.save()
                
                # Also mark the profile as verified
                if hasattr(user, 'profile'):
                    user.profile.email_verified = True
                    user.profile.save()
        
        return user
    
    def populate_user(self, request, sociallogin, data):
        """
        Populate user information from social account data.
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Populate additional fields from Google
        if sociallogin.account.provider == 'google':
            extra_data = sociallogin.account.extra_data
            
            if not user.first_name and extra_data.get('given_name'):
                user.first_name = extra_data.get('given_name', '')
            
            if not user.last_name and extra_data.get('family_name'):
                user.last_name = extra_data.get('family_name', '')
        
        return user
