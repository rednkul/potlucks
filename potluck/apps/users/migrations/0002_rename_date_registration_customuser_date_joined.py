# Generated by Django 3.2.9 on 2022-01-14 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='date_registration',
            new_name='date_joined',
        ),
    ]
