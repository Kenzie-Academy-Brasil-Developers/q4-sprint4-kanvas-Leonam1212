from uuid import uuid4
from django.db import models

# Create your models here.
class Address(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    street = models.CharField(max_length=255)
    house_number = models.IntegerField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    accounts = models.ForeignKey(
        "accounts.Accounts", on_delete=models.CASCADE, related_name="address"
    )
