from django.core.management import BaseCommand
from store import factory


class Command(BaseCommand):
    help = 'Seed Store tables with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Seeding database...'))
        factory.UserFactory.create_batch(2)
        self.stdout.write(self.style.SUCCESS('Database seeded successfully'))
