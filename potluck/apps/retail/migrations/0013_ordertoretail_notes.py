# Generated by Django 3.2.9 on 2022-07-19 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retail', '0012_auto_20220719_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordertoretail',
            name='notes',
            field=models.TextField(blank=True, max_length=200, verbose_name='Примечания к заказу'),
        ),
    ]
