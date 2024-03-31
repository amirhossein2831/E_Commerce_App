from django.core.management import BaseCommand
from django.db import transaction

from store import factory


class Command(BaseCommand):
    help = 'Seed Store tables with sample data'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                # Run the factory here
                factory.AddressFactory.create_user_with_profile_addresses(user_size=10)
                factory.ProductFactory.create_collection_product_promotions_reviews(collections_size=10)
                factory.CartItemFactory.create_cart_cart_items(10)
                factory.OrderItemFactory.create_order_order_items(10)

                self.stdout.write(self.style.SUCCESS('Database seeded successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Database seeding failed: {e}'))