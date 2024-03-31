import factory
from django.conf import settings

from store.models import Customer


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Faker('name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.Faker('password')


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    user = factory.SubFactory(UserFactory)
    phone = factory.Faker('phone_number')
    birth_date = factory.Faker('date_of_birth')
    membership = factory.Faker('random_element', elements=['B', 'S', 'G'])
