from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings


class AuditableModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="+")

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="+")

    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="+")


class Customer(AuditableModel):
    BRONZE_MEMBERSHIP = 'B'
    SILVER_MEMBERSHIP = 'S'
    GOLD_MEMBERSHIP = 'G'

    MEMBERSHIP_PLAN = [
        (BRONZE_MEMBERSHIP, 'BRONZE MEMBERSHIP'),
        (SILVER_MEMBERSHIP, 'SILVER MEMBERSHIP'),
        (GOLD_MEMBERSHIP, 'GOLD MEMBERSHIP'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=11)
    birth_date = models.DateField()
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_PLAN, default=BRONZE_MEMBERSHIP)

    class Meta:
        permissions = [
            ('view_history', 'Can view history')
        ]


class Collection(AuditableModel):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, related_name="+", null=True)


class Promotion(AuditableModel):
    description = models.TextField()
    discount = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])


class Product(AuditableModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=True)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.PositiveIntegerField()
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')
    promotions = models.ManyToManyField(Promotion, related_name='products')


class Review(AuditableModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')


class Address(AuditableModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses', null=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=5, default='-')
