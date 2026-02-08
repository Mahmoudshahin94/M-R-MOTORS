from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import secrets
import os
import uuid

def user_profile_picture_path(instance, filename):
    """Generate upload path for user profile pictures."""
    ext = filename.split('.')[-1]
    filename = f'profile_{instance.user.id}.{ext}'
    return f'profile_pictures/{filename}'

def car_image_path(instance, filename):
    """Generate upload path for car images."""
    ext = filename.split('.')[-1]
    unique_filename = f'{uuid.uuid4().hex}.{ext}'
    return f'car_images/{unique_filename}'

class UserProfile(models.Model):
    """Extended user profile with additional fields."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to=user_profile_picture_path, 
        blank=True, 
        null=True,
        help_text="Upload a profile picture (JPG, PNG, max 5MB)"
    )
    email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, blank=True, null=True)
    reset_token = models.CharField(max_length=255, blank=True, null=True)
    reset_token_created = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def generate_verification_token(self):
        """Generate a unique verification token."""
        self.verification_token = secrets.token_urlsafe(32)
        self.save()
        return self.verification_token

    def generate_reset_token(self):
        """Generate a unique password reset token."""
        from django.utils import timezone
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_created = timezone.now()
        self.save()
        return self.reset_token

    def verify_email(self):
        """Mark email as verified."""
        self.email_verified = True
        self.verification_token = None
        self.save()

    @property
    def is_reset_token_valid(self):
        """Check if reset token is still valid (24 hours)."""
        if not self.reset_token or not self.reset_token_created:
            return False
        from django.utils import timezone
        from datetime import timedelta
        expiry = self.reset_token_created + timedelta(hours=24)
        return timezone.now() < expiry
    
    @property
    def favorite_cars_count(self):
        """Get count of favorite cars."""
        return self.user.favorite_cars.count()


class Car(models.Model):
    """Car model for storing car inventory."""
    title = models.CharField(max_length=255)
    car_model = models.CharField(max_length=255)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    mileage = models.IntegerField(blank=True, null=True)
    condition = models.CharField(max_length=50, blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.year} {self.car_model}"
    
    @property
    def primary_image(self):
        """Get the first image as primary."""
        return self.images.first()


class CarImage(models.Model):
    """Car image model for storing multiple images per car."""
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=car_image_path)
    is_primary = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', 'order', 'created_at']
    
    def __str__(self):
        return f"Image for {self.car}"


class FavoriteCar(models.Model):
    """Track user's favorite cars."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_cars')
    car_id = models.CharField(max_length=255, help_text="InstantDB car post ID")
    car_title = models.CharField(max_length=255, blank=True, null=True)
    car_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    car_image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'car_id')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}'s favorite: {self.car_title or self.car_id}"


class AdminUser(models.Model):
    """Track admin users who can access the admin panel."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_admins')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Admin: {self.user.email}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile whenever a User is created."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the UserProfile whenever the User is saved.
    Made defensive to handle database schema issues during deployment.
    """
    if hasattr(instance, 'profile'):
        try:
            instance.profile.save()
        except Exception as e:
            # Log error but don't fail the user save
            # This handles cases where database schema isn't fully migrated yet
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to save user profile for user {instance.id}: {e}")
