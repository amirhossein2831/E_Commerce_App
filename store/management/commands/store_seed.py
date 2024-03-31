from django.core.management import BaseCommand
from store import factory


class Command(BaseCommand):
    help = 'Seed Store tables with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Seeding database...'))
        # Run the factory here
        # factory.AddressFactory.create_user_with_profile_addresses(user_size=1)
        # factory.ProductFactory.create_collection_product_promotions(collections_size=1)
        self.stdout.write(self.style.SUCCESS('Database seeded successfully'))
