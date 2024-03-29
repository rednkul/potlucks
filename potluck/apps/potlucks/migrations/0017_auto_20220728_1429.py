# Generated by Django 3.2.9 on 2022-07-28 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('potlucks', '0016_auto_20220728_1419'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partorder',
            name='date_send',
        ),
        migrations.RemoveField(
            model_name='partorder',
            name='send',
        ),
        migrations.AddField(
            model_name='part',
            name='date_send',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Дата отправления'),
        ),
        migrations.AddField(
            model_name='part',
            name='send',
            field=models.BooleanField(default=False, verbose_name='Заказ отправлен'),
        ),
    ]
