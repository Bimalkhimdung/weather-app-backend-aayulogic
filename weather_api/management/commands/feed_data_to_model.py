from django.core.management.base import BaseCommand
from weather_api.service import main

class Command(BaseCommand):
    help = 'Feeds data to models from dataset'

    def handle(self, *args, **options):
        main()
        self.stdout.write(self.style.SUCCESS('Migration of data completed successfully.'))