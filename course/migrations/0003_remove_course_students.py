# Generated by Django 4.0.4 on 2022-05-18 20:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_remove_course_instructor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='students',
        ),
    ]
