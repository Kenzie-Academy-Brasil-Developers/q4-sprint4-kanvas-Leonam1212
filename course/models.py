from uuid import uuid4
from django.db import models

# Create your models here.
class Course(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    demo_time = models.TimeField()
    created_at = models.DateField(auto_now_add=True)
    link_repo = models.CharField(max_length=255)
    instructor = models.Field()
    students = models.ManyToManyField("accounts.Accounts", related_name="courses")
