# Generated by Django 3.2.9 on 2022-07-20 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('potlucks', '0011_auto_20220720_1421'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='customer_order',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='products',
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
        migrations.DeleteModel(
            name='RatingStar',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
        migrations.DeleteModel(
            name='Wishlist',
        ),
    ]