import random
import factory
from django.conf import settings

from store.models import *


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Faker('name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.Faker('password')


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    street = factory.Faker('street_address')
    city = factory.Faker('city')
    zip_code = factory.Faker('zipcode')

    @staticmethod
    def create_user_with_profile_addresses(user_size, address_size=2):
        customers = UserFactory.create_batch(user_size)
        [AddressFactory.create_batch(address_size, customer_id=customer.id) for customer in customers]


class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collection

    title = factory.Faker('sentence', nb_words=4)
    featured_product = None


class PromotionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Promotion

    description = factory.Faker('text')
    discount = factory.Faker('random_int', min=1, max=50)


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('text')


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    title = factory.Faker('sentence', nb_words=4)
    slug = factory.Faker('slug')
    description = factory.Faker('text')
    unit_price = factory.Faker('random_int', min=10, max=1000)
    inventory = factory.Faker('random_int', min=0, max=1000)

    @staticmethod
    def create_collection_product_promotions_reviews(collections_size, product_size=5, promotions_size=2,
                                                     review_size=2):
        # create collection
        collections = CollectionFactory.create_batch(collections_size)
        # create product for each collection
        products_list = [ProductFactory.create_batch(product_size, collection=collection) for collection in collections]

        for products in products_list:
            for product in products:
                # create review for each product
                ReviewFactory.create_batch(review_size, product=product)
                # create promotions for each product
                promotions = PromotionFactory.create_batch(promotions_size)
                product.promotions.set(promotions)
                product.save()


class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart


class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem

    quantity = random.randint(0, 10)

    @staticmethod
    def create_cart_cart_items(cart_size, item_size=5):
        product_ids = Product.objects.only('id').values_list('id', flat=True)

        carts = CartFactory.create_batch(cart_size)
        for cart in carts:
            for _ in range(item_size):
                CartItemFactory.create(cart=cart, product_id=random.choice(product_ids))
