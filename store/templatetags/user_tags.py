from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='is_admin')
def is_admin(user):
    """Check if user is an admin based on email."""
    if not user or not user.is_authenticated:
        return False
    return user.email in settings.ADMIN_EMAILS
