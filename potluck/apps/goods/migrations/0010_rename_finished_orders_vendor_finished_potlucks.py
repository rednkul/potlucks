# Generated by Django 3.2.9 on 2022-07-28 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0009_alter_product_parameters'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vendor',
            old_name='finished_orders',
            new_name='finished_potlucks',
        ),
    ]
