# Generated by Django 3.2.9 on 2022-08-14 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name': 'Адрес', 'verbose_name_plural': 'Адреса'},
        ),
        migrations.AlterModelOptions(
            name='email',
            options={'verbose_name': 'Контактный email', 'verbose_name_plural': 'Контактные email'},
        ),
        migrations.AlterModelOptions(
            name='phonenumber',
            options={'verbose_name': 'Контактный номер телефона', 'verbose_name_plural': 'Контактные номера телефонов'},
        ),
    ]