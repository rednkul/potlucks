# Generated by Django 3.2.9 on 2022-01-20 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20220118_1229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='patrynomic',
        ),
        migrations.AlterField(
            model_name='profile',
            name='instagram',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Профиль instagram'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='telegram',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Профиль telegram'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='vk',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Профиль ВКонтакте'),
        ),
    ]