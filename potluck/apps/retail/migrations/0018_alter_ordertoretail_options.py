# Generated by Django 3.2.9 on 2022-07-28 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('retail', '0017_remove_orderitem_updated_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ordertoretail',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
    ]
