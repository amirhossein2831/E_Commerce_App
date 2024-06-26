from django.core.management import BaseCommand
from django.db import transaction

from store import factories


class Command(BaseCommand):
    help = 'Seed Store tables with sample data'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                self.stdout.write(self.style.SUCCESS('Seeding database...'))

                factories.AddressFactory.create_user_with_profile_addresses(user_size=10)
                factories.ProductFactory.create_collection_product_promotions_reviews(collections_size=10)
                factories.CartItemFactory.create_cart_cart_items(10)
                factories.OrderItemFactory.create_order_order_items(10)

                self.stdout.write(self.style.SUCCESS('Database seeded successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Database seeding failed: {e}'))
