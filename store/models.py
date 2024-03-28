from django.db import models
from django.conf import settings
from common.models import AuditableModel



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
