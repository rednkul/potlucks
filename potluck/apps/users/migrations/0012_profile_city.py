# Generated by Django 3.2.9 on 2022-07-18 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_rename_patrynomic_profile_patronymic'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, max_length=100, verbose_name='Город'),
        ),
    ]
