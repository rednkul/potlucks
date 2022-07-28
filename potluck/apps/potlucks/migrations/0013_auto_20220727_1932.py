# Generated by Django 3.2.9 on 2022-07-27 12:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('potlucks', '0012_auto_20220720_1545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerorder',
            name='date',
        ),
        migrations.RemoveField(
            model_name='customerorder',
            name='send',
        ),
        migrations.AddField(
            model_name='customerorder',
            name='city',
            field=models.CharField(default='Барабибирск', max_length=100, verbose_name='Город'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customerorder',
            name='confirmed',
            field=models.BooleanField(default=False, verbose_name='Подтвержден'),
        ),
        migrations.AddField(
            model_name='customerorder',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customerorder',
            name='email',
            field=models.EmailField(default='kalapaka@mail.com', max_length=254, verbose_name='Адрес электронной почты'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customerorder',
            name='first_name',
            field=models.CharField(default='Чупке', max_length=30, verbose_name='Имя'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customerorder',
            name='last_name',
            field=models.CharField(default='Чупке', max_length=30, verbose_name='Фамилия'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customerorder',
            name='patronymic',
            field=models.CharField(blank=True, max_length=30, verbose_name='Отчество'),
        ),
        migrations.AddField(
            model_name='customerorder',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, verbose_name='Номер телефона'),
        ),
        migrations.AddField(
            model_name='customerorder',
            name='post_index',
            field=models.CharField(blank=True, max_length=6, verbose_name='Почтовый индекс'),
        ),
    ]
