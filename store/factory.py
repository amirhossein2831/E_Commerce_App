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
