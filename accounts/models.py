from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Accounts(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    username = models.CharField(unique=False, null=True, max_length=255)

    address = models.ForeignKey("address.Address", on_delete=models.CASCADE, related_name="users")
    
    course = models.OneToOneField("course.Course", null=True, on_delete=models.CASCADE)
   
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
