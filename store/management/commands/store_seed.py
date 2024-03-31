from django.core.management import BaseCommand
from store import factory
from store.models import Address


class Command(BaseCommand):
    help = 'Seed Store tables with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Seeding database...'))
        factory.AddressFactory.create_user_with_profile_addresses(user_size=1)
        self.stdout.write(self.style.SUCCESS('Database seeded successfully'))
