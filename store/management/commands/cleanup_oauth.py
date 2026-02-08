from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    help = 'Clean up duplicate Google OAuth SocialApp entries'

    def handle(self, *args, **options):
        """Remove all SocialApp entries since we use settings-based config."""
        
        # Count existing Google apps
        google_apps = SocialApp.objects.filter(provider='google')
        count = google_apps.count()
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS('No Google OAuth SocialApp entries found. Using settings-based config.'))
            return
        
        self.stdout.write(f'Found {count} Google OAuth SocialApp entries in database.')
        
        # Delete all SocialApp entries for Google since we use settings-based config
        deleted_count, _ = google_apps.delete()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully removed {deleted_count} Google OAuth SocialApp entries. '
                f'Now using settings-based configuration from settings.py'
            )
        )
