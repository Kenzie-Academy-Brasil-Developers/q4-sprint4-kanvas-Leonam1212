# Generated by Django 4.0.4 on 2022-05-20 18:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0003_remove_course_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(related_name='courses', to=settings.AUTH_USER_MODEL),
        ),
    ]
