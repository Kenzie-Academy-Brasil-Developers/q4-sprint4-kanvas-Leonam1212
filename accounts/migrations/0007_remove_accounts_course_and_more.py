# Generated by Django 4.0.4 on 2022-05-20 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_accounts_instructor_course_remove_accounts_course_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accounts',
            name='course',
        ),
        migrations.RemoveField(
            model_name='accounts',
            name='instructor_course',
        ),
    ]