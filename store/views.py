from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import UserProfile, FavoriteCar, Car, CarImage, AdminUser
import json
import logging

logger = logging.getLogger(__name__)

def home(request):
    """Render the home page."""
    return render(request, 'home.html')

def inventory(request):
    """Render the inventory page."""
    return render(request, 'inventory.html')

def car_detail(request, car_id):
    """Render the car detail page."""
    context = {
        'car_id': car_id
    }
    return render(request, 'car_detail.html', context)

def location(request):
    """Render the location page."""
    return render(request, 'location.html')

@login_required
def admin_panel(request):
    """Render the admin panel page - restricted to admin users."""
    # Check if user is admin (either in ADMIN_EMAILS or has AdminUser record)
    is_admin = (request.user.email in settings.ADMIN_EMAILS or 
                hasattr(request.user, 'admin_profile'))
    
    if not is_admin:
        messages.error(request, 'You do not have permission to access the admin panel.')
        return redirect('home')
    
    return render(request, 'admin_panel.html')

def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        # Try to get user by email
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html')
        except Exception as e:
            messages.error(request, 'Login temporarily unavailable. Please try again later.')
            return render(request, 'login.html')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            
            # Set session expiry
            if not remember_me:
                request.session.set_expiry(0)  # Session expires when browser closes
            
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'login.html')

def signup_view(request):
    """Handle user signup."""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validate passwords match
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'login.html')
        
        # Check if email already exists
        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            if existing_user.profile.email_verified:
                messages.error(request, '❌ This email address is already verified and in use. Please use a different email or log in to your existing account.')
            else:
                messages.error(request, '❌ An account with this email already exists. Please log in or use a different email.')
            return render(request, 'login.html')
        
        # Create username from email
        username = email.split('@')[0]
        
        # If username exists, append numbers
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        # Parse full name
        name_parts = full_name.strip().split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Log the user in
            auth_login(request, user)
            
            # Try to send verification email (don't fail signup if this fails)
            email_sent = False
            try:
                token = user.profile.generate_verification_token()
                send_verification_email(user, token)
                email_sent = True
            except Exception as email_error:
                logger.error(f"Failed to send verification email during signup: {email_error}")
                # Continue with signup even if email fails
            
            # Show appropriate success message
            if email_sent:
                messages.success(request, f'✅ Welcome to M&R Motors, {first_name}! Please check your email to verify your account.')
            else:
                messages.warning(request, f'✅ Welcome to M&R Motors, {first_name}! You can send a verification email from your profile.')
            
            return redirect('profile')
            
        except Exception as e:
            logger.error(f"Error during user creation: {e}")
            messages.error(request, '❌ An error occurred during signup. Please try again.')
            return render(request, 'login.html')
    
    return render(request, 'login.html')

def logout_view(request):
    """Handle user logout."""
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

def password_reset_request(request):
    """Handle password reset request."""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            token = user.profile.generate_reset_token()
            
            # Send password reset email
            send_password_reset_email(user, token)
            
            messages.success(request, 'Password reset instructions have been sent to your email.')
        except User.DoesNotExist:
            # Don't reveal that the user doesn't exist
            messages.success(request, 'If an account exists with this email, password reset instructions have been sent.')
        
        return redirect('login')
    
    return render(request, 'password_reset.html')

def password_reset_confirm(request, token):
    """Handle password reset confirmation."""
    try:
        profile = UserProfile.objects.get(reset_token=token)
        
        if not profile.is_reset_token_valid:
            messages.error(request, 'This password reset link has expired. Please request a new one.')
            return redirect('password_reset')
        
        if request.method == 'POST':
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            
            if password != password_confirm:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'password_reset_confirm.html')
            
            # Update password
            user = profile.user
            user.set_password(password)
            user.save()
            
            # Clear reset token
            profile.reset_token = None
            profile.reset_token_created = None
            profile.save()
            
            messages.success(request, 'Your password has been reset successfully. Please log in.')
            return redirect('login')
        
        return render(request, 'password_reset_confirm.html')
        
    except UserProfile.DoesNotExist:
        messages.error(request, 'Invalid password reset link.')
        return redirect('password_reset')

def verify_email(request, token):
    """Handle email verification via token link."""
    try:
        profile = UserProfile.objects.get(verification_token=token)
        
        # Check if this email is already verified by another user
        email_to_verify = profile.user.email
        already_verified_user = User.objects.filter(
            email=email_to_verify,
            profile__email_verified=True
        ).exclude(id=profile.user.id).first()
        
        if already_verified_user:
            messages.error(request, f'❌ This email address is already verified and in use by another account. Please use a different email address.')
            return redirect('profile') if request.user.is_authenticated else redirect('login')
        
        # Verify the email
        profile.verify_email()
        
        messages.success(request, '✅ Your email has been verified successfully!')
        return redirect('profile') if request.user.is_authenticated else redirect('login')
        
    except UserProfile.DoesNotExist:
        messages.error(request, '❌ Invalid or expired verification link.')
        return redirect('home')

@login_required
def verify_email_prompt(request):
    """Show email verification code entry form."""
    if request.user.profile.email_verified:
        messages.info(request, 'Your email is already verified.')
        return redirect('profile')
    
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        
        if request.user.profile.is_verification_code_valid(code):
            request.user.profile.verify_email()
            messages.success(request, 'Your email has been verified successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Invalid or expired verification code. Please try again or request a new code.')
    
    return render(request, 'verify_email_code.html')

def verify_email_sent(request, email):
    """Show email verification sent page."""
    return render(request, 'verify_email.html', {'email': email})

def resend_verification(request):
    """Resend verification email."""
    # Check if user is authenticated
    if request.user.is_authenticated:
        user = request.user
        
        # Check if user signed up via Google (social account)
        if user.socialaccount_set.filter(provider='google').exists():
            # Mark as verified since Google already verified the email
            user.profile.email_verified = True
            user.profile.save()
            messages.success(request, 'Your email has been verified via Google.')
            return redirect('profile')
        
        # Check if already verified
        if user.profile.email_verified:
            messages.info(request, 'Your email is already verified.')
            return redirect('profile')
        
        # Send verification email with link
        try:
            token = user.profile.generate_verification_token()
            send_verification_email(user, token)
            messages.success(request, '✅ Verification email has been sent successfully! Please check your inbox and click the link to verify.')
        except Exception as e:
            logger.error(f'Failed to send verification email: {str(e)}')
            messages.error(request, f'Failed to send verification email. Please try again later.')
        
        return redirect('profile')
    
    # If not authenticated and POST request
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            
            if user.profile.email_verified:
                messages.info(request, 'Your email is already verified.')
                return redirect('login')
            
            code = user.profile.generate_verification_code()
            send_verification_email_with_code(user, code)
            
            messages.success(request, 'Verification email has been resent.')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')
    
    return redirect('login')

@login_required
def verify_phone_prompt(request):
    """Show phone verification code entry form."""
    if not request.user.profile.phone_number:
        messages.error(request, 'Please add a phone number to your profile first.')
        return redirect('profile')
    
    if request.user.profile.phone_verified:
        messages.info(request, 'Your phone number is already verified.')
        return redirect('profile')
    
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        
        if request.user.profile.is_phone_verification_code_valid(code):
            request.user.profile.verify_phone()
            messages.success(request, 'Your phone number has been verified successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Invalid or expired verification code. Please try again or request a new code.')
    else:
        # Automatically send code when page is loaded for the first time
        try:
            code = request.user.profile.generate_phone_verification_code()
            send_phone_verification_sms(request.user, code)
            messages.info(request, f'Verification code sent to {request.user.profile.phone_number}')
        except Exception as e:
            logger.error(f'Error sending phone verification on page load: {e}')
            messages.warning(request, 'Failed to send verification code automatically. Please use the resend button.')
    
    return render(request, 'verify_phone_code.html')

@login_required
@require_POST
def send_phone_verification(request):
    """Send phone verification SMS."""
    if not request.user.profile.phone_number:
        return JsonResponse({'success': False, 'error': 'No phone number set'}, status=400)
    
    if request.user.profile.phone_verified:
        return JsonResponse({'success': False, 'error': 'Phone already verified'}, status=400)
    
    try:
        code = request.user.profile.generate_phone_verification_code()
        success = send_phone_verification_sms(request.user, code)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': 'Verification code sent to your phone'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Failed to send SMS. Please check your phone number.'
            }, status=500)
    except Exception as e:
        logger.error(f'Error sending phone verification: {e}')
        return JsonResponse({
            'success': False,
            'error': 'Failed to send verification code'
        }, status=500)

@login_required
def profile_view(request):
    """Display user profile."""
    # Ensure user has a profile (it should be auto-created, but just in case)
    if not hasattr(request.user, 'profile'):
        UserProfile.objects.create(user=request.user)
    
    return render(request, 'profile.html')

@login_required
def update_profile(request):
    """Update user profile information."""
    if request.method == 'POST':
        try:
            user = request.user
            
            # Ensure user has a profile
            if not hasattr(user, 'profile'):
                UserProfile.objects.create(user=user)
            
            user.first_name = request.POST.get('first_name', '').strip()
            user.last_name = request.POST.get('last_name', '').strip()
            new_email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            
            # Handle profile picture upload
            if 'profile_picture' in request.FILES:
                profile_picture = request.FILES['profile_picture']
                
                # Validate file size (max 5MB)
                if profile_picture.size > 5 * 1024 * 1024:
                    messages.error(request, 'Profile picture must be less than 5MB.')
                    return redirect('profile')
                
                # Validate file type
                allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
                if profile_picture.content_type not in allowed_types:
                    messages.error(request, 'Profile picture must be a valid image file (JPG, PNG, GIF, WEBP).')
                    return redirect('profile')
                
                # Delete old profile picture if exists (safely)
                try:
                    if user.profile.profile_picture:
                        user.profile.profile_picture.delete(save=False)
                except Exception:
                    pass  # Ignore deletion errors
                
                user.profile.profile_picture = profile_picture
            
            # Check if email changed and if it's already taken
            if new_email != user.email:
                # Check if email is already in use (including by verified users)
                existing_user = User.objects.filter(email=new_email).exclude(id=user.id).first()
                if existing_user:
                    if existing_user.profile.email_verified:
                        messages.error(request, '❌ This email address is already verified and in use by another account. Please use a different email.')
                    else:
                        messages.error(request, '❌ This email address is already in use by another account.')
                    return redirect('profile')
                
                user.email = new_email
                user.profile.email_verified = False
                user.profile.save()
                
                # Send new verification email with link
                try:
                    token = user.profile.generate_verification_token()
                    send_verification_email(user, token)
                    messages.warning(request, '⚠️ Email updated. Please check your new email to verify it.')
                except Exception:
                    messages.warning(request, '⚠️ Email updated but failed to send verification email. You can request a new one from your profile.')
            
            user.save()
            
            # Update phone number
            old_phone = user.profile.phone_number
            if phone and phone != old_phone:
                user.profile.phone_number = phone
                user.profile.phone_verified = False  # Mark as unverified if changed
                user.profile.save()
                
                # Only show phone warning if email didn't change
                if new_email == user.email:
                    messages.success(request, '✅ Profile updated! Please verify your new phone number.')
            else:
                user.profile.phone_number = phone
                user.profile.save()
                
                # Only show success if email and phone didn't change
                if new_email == user.email and phone == old_phone:
                    messages.success(request, '✅ Profile updated successfully!')
            
        except Exception as e:
            messages.error(request, f'❌ Error updating profile: {str(e)}')
            return redirect('profile')
    
    return redirect('profile')

@login_required
def remove_profile_picture(request):
    """Remove user's profile picture."""
    if request.method == 'POST':
        user = request.user
        if user.profile.profile_picture:
            user.profile.profile_picture.delete(save=True)
            messages.success(request, 'Profile picture removed successfully!')
        else:
            messages.info(request, 'No profile picture to remove.')
    
    return redirect('profile')

@login_required
def change_password(request):
    """Change user password."""
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')
        
        user = request.user
        
        # Verify current password
        if not user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('profile')
        
        # Check passwords match
        if new_password != confirm_new_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('profile')
        
        # Update password
        user.set_password(new_password)
        user.save()
        
        # Update session to prevent logout
        update_session_auth_hash(request, user)
        
        messages.success(request, 'Password changed successfully!')
    
    return redirect('profile')

@login_required
def delete_account(request):
    """Delete user account."""
    if request.method == 'POST' or request.method == 'GET':
        user = request.user
        auth_logout(request)
        user.delete()
        
        messages.success(request, 'Your account has been deleted.')
        return redirect('home')
    
    return redirect('profile')

# Favorite Cars Views
@login_required
def favorites_view(request):
    """Display user's favorite cars."""
    favorites = FavoriteCar.objects.filter(user=request.user)
    context = {
        'favorites': favorites,
        'favorites_count': favorites.count()
    }
    return render(request, 'favorites.html', context)

@login_required
@require_POST
def add_to_favorites(request):
    """Add a car to user's favorites."""
    try:
        data = json.loads(request.body)
        car_id = data.get('car_id')
        car_title = data.get('car_title', '')
        car_price = data.get('car_price', 0)
        car_image_url = data.get('car_image_url', '')
        
        if not car_id:
            return JsonResponse({'success': False, 'error': 'Car ID is required'}, status=400)
        
        # Check if already favorited
        favorite, created = FavoriteCar.objects.get_or_create(
            user=request.user,
            car_id=car_id,
            defaults={
                'car_title': car_title,
                'car_price': car_price,
                'car_image_url': car_image_url
            }
        )
        
        if created:
            return JsonResponse({
                'success': True, 
                'message': 'Added to favorites!',
                'action': 'added'
            })
        else:
            return JsonResponse({
                'success': True, 
                'message': 'Already in favorites',
                'action': 'exists'
            })
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_POST
def remove_from_favorites(request):
    """Remove a car from user's favorites."""
    try:
        data = json.loads(request.body)
        car_id = data.get('car_id')
        
        if not car_id:
            return JsonResponse({'success': False, 'error': 'Car ID is required'}, status=400)
        
        deleted_count, _ = FavoriteCar.objects.filter(
            user=request.user,
            car_id=car_id
        ).delete()
        
        if deleted_count > 0:
            return JsonResponse({
                'success': True,
                'message': 'Removed from favorites',
                'action': 'removed'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Favorite not found'
            }, status=404)
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def check_favorite(request, car_id):
    """Check if a car is in user's favorites."""
    is_favorite = FavoriteCar.objects.filter(
        user=request.user,
        car_id=car_id
    ).exists()
    
    return JsonResponse({'is_favorite': is_favorite})

@login_required
def get_user_favorites(request):
    """Get list of user's favorite car IDs."""
    favorite_ids = list(
        FavoriteCar.objects.filter(user=request.user)
        .values_list('car_id', flat=True)
    )
    
    return JsonResponse({'favorite_ids': favorite_ids})

# Helper functions for sending emails
def send_verification_email(user, token):
    """Send email verification link (old method for backwards compatibility)."""
    verification_url = f"{settings.SITE_URL}/verify-email/{token}/"
    
    subject = 'Verify Your Email - M&R Motors'
    message = f"""
    Hi {user.first_name},
    
    Thank you for signing up at M&R Motors!
    
    Please click the link below to verify your email address:
    {verification_url}
    
    If you didn't create an account, please ignore this email.
    
    Best regards,
    M&R Motors Team
    """
    
    try:
        logger.info(f"Attempting to send verification email to {user.email}")
        logger.info(f"Email settings - Backend: {settings.EMAIL_BACKEND}, Host: {settings.EMAIL_HOST}, User: {settings.EMAIL_HOST_USER}")
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        logger.info(f"✓ Verification email sent successfully to {user.email}")
    except Exception as e:
        logger.error(f"✗ Error sending email to {user.email}: {str(e)}")
        logger.error(f"Email backend: {settings.EMAIL_BACKEND}")
        logger.error(f"Email host: {settings.EMAIL_HOST}")
        logger.error(f"Email user: {settings.EMAIL_HOST_USER}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        # Don't raise in production to avoid breaking the signup flow
        # but log the error so we can see what went wrong

def send_verification_email_with_code(user, code):
    """Send email verification with 6-digit code."""
    subject = 'Verify Your Email - M&R Motors'
    message = f"""
    Hi {user.first_name},
    
    Thank you for signing up at M&R Motors!
    
    Your email verification code is: {code}
    
    This code will expire in 10 minutes.
    
    Please enter this code on the verification page to complete your registration.
    
    If you didn't create an account, please ignore this email.
    
    Best regards,
    M&R Motors Team
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        logger.info(f"Verification code email sent successfully to {user.email}")
    except Exception as e:
        logger.error(f"Error sending verification code email to {user.email}: {str(e)}")
        raise

def send_password_reset_email(user, token):
    """Send password reset link."""
    reset_url = f"{settings.SITE_URL}/password-reset/{token}/"
    
    subject = 'Reset Your Password - M&R Motors'
    message = f"""
    Hi {user.first_name},
    
    You requested to reset your password at M&R Motors.
    
    Please click the link below to reset your password:
    {reset_url}
    
    This link will expire in 24 hours.
    
    If you didn't request this, please ignore this email.
    
    Best regards,
    M&R Motors Team
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        logger.info(f"Password reset email sent successfully to {user.email}")
    except Exception as e:
        logger.error(f"Error sending password reset email to {user.email}: {str(e)}")
        raise

def test_email_config(request):
    """Test endpoint to check email configuration."""
    from django.http import HttpResponse
    import traceback
    
    config = {
        'EMAIL_BACKEND': settings.EMAIL_BACKEND,
        'EMAIL_HOST': settings.EMAIL_HOST,
        'EMAIL_PORT': settings.EMAIL_PORT,
        'EMAIL_USE_TLS': settings.EMAIL_USE_TLS,
        'EMAIL_HOST_USER': settings.EMAIL_HOST_USER,
        'EMAIL_HOST_PASSWORD': '***SET***' if settings.EMAIL_HOST_PASSWORD else '⚠️ NOT SET',
        'DEFAULT_FROM_EMAIL': settings.DEFAULT_FROM_EMAIL,
        'SITE_URL': settings.SITE_URL,
    }
    
    html = "<h1>Email Configuration Diagnostic</h1><ul>"
    for key, value in config.items():
        html += f"<li><strong>{key}:</strong> {value}</li>"
    html += "</ul>"
    
    # Try to send a test email if user is authenticated
    if request.user.is_authenticated:
        html += "<hr><h2>Test Email</h2>"
        try:
            send_mail(
                'Test Email from M&R Motors',
                'This is a test email to verify your email configuration is working.',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )
            html += f"<p style='color: green; font-size: 18px;'>✓ Test email sent successfully to <strong>{request.user.email}</strong>!</p>"
            html += "<p>Check your inbox (and spam folder).</p>"
        except Exception as e:
            html += f"<p style='color: red; font-size: 18px;'>✗ Error sending test email:</p>"
            html += f"<p style='color: red;'><strong>{str(e)}</strong></p>"
            html += f"<pre style='background: #f5f5f5; padding: 10px; overflow-x: auto;'>{traceback.format_exc()}</pre>"
    else:
        html += "<hr><p>Log in to test sending an email.</p>"
    
    return HttpResponse(html)

def send_phone_verification_sms(user, code):
    """Send SMS verification code using Twilio."""
    try:
        from twilio.rest import Client
        
        # Get Twilio credentials from settings
        account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
        auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
        from_number = getattr(settings, 'TWILIO_PHONE_NUMBER', None)
        
        if not all([account_sid, auth_token, from_number]):
            logger.warning('Twilio credentials not configured. SMS not sent.')
            # In development, just log the code
            logger.info(f'Phone verification code for {user.email}: {code}')
            print(f'📱 Phone verification code for {user.email}: {code}')
            return True  # Return True in development mode
        
        client = Client(account_sid, auth_token)
        
        message_body = f"""M&R Motors

Your phone verification code is: {code}

This code will expire in 10 minutes.

If you didn't request this, please ignore this message."""
        
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=user.profile.phone_number
        )
        
        logger.info(f'SMS sent successfully. SID: {message.sid}')
        return True
    except ImportError:
        logger.warning('Twilio not installed. SMS not sent.')
        # In development, just log the code
        logger.info(f'Phone verification code for {user.email}: {code}')
        print(f'📱 Phone verification code for {user.email}: {code}')
        return True
    except Exception as e:
        logger.error(f'Error sending SMS: {e}')
        # In development, just log the code
        logger.info(f'Phone verification code for {user.email}: {code}')
        print(f'📱 Phone verification code for {user.email}: {code}')
        return False


# Car Management Views
@login_required
def add_car_view(request):
    """Add a new car with image uploads."""
    is_admin = (request.user.email in settings.ADMIN_EMAILS or 
                hasattr(request.user, 'admin_profile'))
    
    if not is_admin:
        messages.error(request, 'You do not have permission to add cars.')
        return redirect('home')
    
    if request.method == 'POST':
        try:
            # Create car
            car = Car.objects.create(
                title=request.POST.get('title'),
                car_model=request.POST.get('car_model'),
                year=int(request.POST.get('year')),
                price=float(request.POST.get('price')),
                description=request.POST.get('description'),
                mileage=request.POST.get('mileage') or None,
                condition=request.POST.get('condition') or None,
            )
            
            # Handle multiple image uploads
            images = request.FILES.getlist('images')
            for idx, image in enumerate(images):
                CarImage.objects.create(
                    car=car,
                    image=image,
                    is_primary=(idx == 0),
                    order=idx
                )
            
            messages.success(request, 'Car added successfully!')
            return JsonResponse({'success': True, 'car_id': car.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


def get_cars_api(request):
    """Get all cars as JSON. Only shows non-hidden cars to public."""
    # Filter out hidden cars from public view
    cars = Car.objects.filter(is_hidden=False)
    cars_data = []
    
    for car in cars:
        images = [{'url': img.image.url, 'is_primary': img.is_primary} for img in car.images.all()]
        cars_data.append({
            'id': car.id,
            'title': car.title,
            'car_model': car.car_model,
            'year': car.year,
            'price': float(car.price),
            'description': car.description,
            'mileage': car.mileage,
            'condition': car.condition,
            'is_sold': car.is_sold,
            'is_hidden': car.is_hidden,
            'images': images,
            'primary_image': car.primary_image.image.url if car.primary_image else None,
            'created_at': car.created_at.isoformat(),
        })
    
    return JsonResponse({'cars': cars_data})


@login_required
def get_admin_cars_api(request):
    """Get all cars including hidden ones for admin panel."""
    is_admin = (request.user.email in settings.ADMIN_EMAILS or 
                hasattr(request.user, 'admin_profile'))
    
    if not is_admin:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    # Show ALL cars for admin, including hidden ones
    cars = Car.objects.all()
    cars_data = []
    
    for car in cars:
        images = [{'id': img.id, 'url': img.image.url, 'is_primary': img.is_primary} for img in car.images.all()]
        cars_data.append({
            'id': car.id,
            'title': car.title,
            'car_model': car.car_model,
            'year': car.year,
            'price': float(car.price),
            'description': car.description,
            'mileage': car.mileage,
            'condition': car.condition,
            'is_sold': car.is_sold,
            'is_hidden': car.is_hidden,
            'images': images,
            'primary_image': car.primary_image.image.url if car.primary_image else None,
            'created_at': car.created_at.isoformat(),
        })
    
    return JsonResponse({'cars': cars_data})


@login_required
@require_POST
def update_car_view(request, car_id):
    """Update a car."""
    is_admin = (request.user.email in settings.ADMIN_EMAILS or 
                hasattr(request.user, 'admin_profile'))
    
    if not is_admin:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    try:
        from django.db.models import Max
        car = get_object_or_404(Car, id=car_id)
        
        car.title = request.POST.get('title', car.title)
        car.car_model = request.POST.get('car_model', car.car_model)
        car.year = int(request.POST.get('year', car.year))
        car.price = float(request.POST.get('price', car.price))
        car.description = request.POST.get('description', car.description)
        car.mileage = request.POST.get('mileage') or car.mileage
        car.condition = request.POST.get('condition') or car.condition
        car.save()
        
        # Handle new images if uploaded
        new_images = request.FILES.getlist('images')
        if new_images:
            # Get current max order
            max_order = car.images.aggregate(Max('order'))['order__max'] or 0
            for idx, image in enumerate(new_images):
                CarImage.objects.create(
                    car=car,
                    image=image,
                    is_primary=False,
                    order=max_order + idx + 1
                )
        
        messages.success(request, 'Car updated successfully!')
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def delete_car_view(request, car_id):
    """Delete a car."""
    is_admin = (request.user.email in settings.ADMIN_EMAILS or 
                hasattr(request.user, 'admin_profile'))
    
    if not is_admin:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    try:
        car = get_object_or_404(Car, id=car_id)
        car.delete()
        messages.success(request, 'Car deleted successfully!')
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def delete_car_image_view(request, image_id):
    """Delete a car image."""
    is_admin = (request.user.email in settings.ADMIN_EMAILS or 
                hasattr(request.user, 'admin_profile'))
    
    if not is_admin:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    try:
        image = get_object_or_404(CarImage, id=image_id)
        image.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def toggle_car_sold_status(request, car_id):
    """Toggle the sold status of a car."""
    is_admin = (request.user.email in settings.ADMIN_EMAILS or 
                hasattr(request.user, 'admin_profile'))
    
    if not is_admin:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    try:
        car = get_object_or_404(Car, id=car_id)
        car.is_sold = not car.is_sold
        car.save()
        
        status = 'sold' if car.is_sold else 'available'
        messages.success(request, f'Car marked as {status}!')
        return JsonResponse({'success': True, 'is_sold': car.is_sold})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def toggle_car_hidden_status(request, car_id):
    """Toggle the hidden status of a car."""
    is_admin = (request.user.email in settings.ADMIN_EMAILS or 
                hasattr(request.user, 'admin_profile'))
    
    if not is_admin:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    try:
        car = get_object_or_404(Car, id=car_id)
        car.is_hidden = not car.is_hidden
        car.save()
        
        status = 'hidden' if car.is_hidden else 'visible'
        messages.success(request, f'Car is now {status} in the inventory!')
        return JsonResponse({'success': True, 'is_hidden': car.is_hidden})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


# Admin User Management Views
@login_required
def get_admin_users(request):
    """Get all admin users."""
    is_admin = (request.user.email in settings.ADMIN_EMAILS or 
                hasattr(request.user, 'admin_profile'))
    
    if not is_admin:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    admin_users = AdminUser.objects.select_related('user', 'created_by').all()
    admins_data = []
    
    for admin in admin_users:
        admins_data.append({
            'id': admin.id,
            'user_id': admin.user.id,
            'email': admin.user.email,
            'first_name': admin.user.first_name,
            'last_name': admin.user.last_name,
            'created_by': admin.created_by.email if admin.created_by else 'System',
            'created_at': admin.created_at.isoformat(),
        })
    
    return JsonResponse({'admins': admins_data})


@login_required
@require_POST
def add_admin_user(request):
    """Add a new admin user."""
    is_admin = (request.user.email in settings.ADMIN_EMAILS or 
                hasattr(request.user, 'admin_profile'))
    
    if not is_admin:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    try:
        data = json.loads(request.body)
        email = data.get('email')
        
        if not email:
            return JsonResponse({'success': False, 'error': 'Email is required'}, status=400)
        
        # Check if user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User with this email does not exist'}, status=404)
        
        # Check if already an admin
        if AdminUser.objects.filter(user=user).exists():
            return JsonResponse({'success': False, 'error': 'User is already an admin'}, status=400)
        
        # Create admin user
        admin_user = AdminUser.objects.create(
            user=user,
            created_by=request.user
        )
        
        return JsonResponse({
            'success': True,
            'admin': {
                'id': admin_user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def remove_admin_user(request, admin_id):
    """Remove an admin user."""
    is_admin = (request.user.email in settings.ADMIN_EMAILS or 
                hasattr(request.user, 'admin_profile'))
    
    if not is_admin:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    try:
        admin_user = get_object_or_404(AdminUser, id=admin_id)
        
        # Prevent removing yourself
        if admin_user.user == request.user:
            return JsonResponse({'success': False, 'error': 'You cannot remove yourself as admin'}, status=400)
        
        admin_user.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
