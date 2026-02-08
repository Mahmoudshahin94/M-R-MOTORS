from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection


class Command(BaseCommand):
    help = 'Run migrations with verbose output for production debugging'

    def handle(self, *args, **options):
        """Run migrations with detailed output."""
        
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('RUNNING PRODUCTION MIGRATIONS'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        
        # Test database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version()")
                version = cursor.fetchone()
                self.stdout.write(f'Database: {version[0]}')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Database connection failed: {e}'))
            return
        
        # Show pending migrations
        self.stdout.write('\nChecking for pending migrations...')
        call_command('showmigrations', '--plan')
        
        # Run migrations
        self.stdout.write('\nApplying migrations...')
        call_command('migrate', '--noinput', verbosity=2)
        
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 50))
        self.stdout.write(self.style.SUCCESS('MIGRATIONS COMPLETED'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
