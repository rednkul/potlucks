# Generated by Django 3.2.9 on 2022-07-19 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retail', '0011_auto_20220718_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordertoretail',
            name='patronymic',
            field=models.CharField(blank=True, max_length=30, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='ordertoretail',
            name='address',
            field=models.CharField(max_length=100, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='ordertoretail',
            name='city',
            field=models.CharField(max_length=100, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='ordertoretail',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='ordertoretail',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='Фамилия'),
        ),
    ]