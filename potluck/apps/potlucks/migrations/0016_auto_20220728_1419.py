# Generated by Django 3.2.9 on 2022-07-28 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('potlucks', '0015_auto_20220728_0122'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='part',
            options={'verbose_name': 'Доля пользователя в складчине', 'verbose_name_plural': 'Доли пользователей в складчинах'},
        ),
        migrations.RemoveField(
            model_name='part',
            name='address',
        ),
        migrations.RemoveField(
            model_name='part',
            name='city',
        ),
        migrations.RemoveField(
            model_name='part',
            name='confirmed',
        ),
        migrations.RemoveField(
            model_name='part',
            name='date_send',
        ),
        migrations.RemoveField(
            model_name='part',
            name='email',
        ),
        migrations.RemoveField(
            model_name='part',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='part',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='part',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='part',
            name='paid',
        ),
        migrations.RemoveField(
            model_name='part',
            name='patronymic',
        ),
        migrations.RemoveField(
            model_name='part',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='part',
            name='post_index',
        ),
        migrations.RemoveField(
            model_name='part',
            name='send',
        ),
        migrations.AddField(
            model_name='part',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='PartOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Адрес электронной почты')),
                ('phone_number', models.CharField(blank=True, max_length=15, verbose_name='Номер телефона')),
                ('patronymic', models.CharField(blank=True, max_length=30, verbose_name='Отчество')),
                ('first_name', models.CharField(max_length=30, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=30, verbose_name='Фамилия')),
                ('city', models.CharField(max_length=100, verbose_name='Город')),
                ('post_index', models.CharField(blank=True, max_length=6, verbose_name='Почтовый индекс')),
                ('address', models.CharField(max_length=100, verbose_name='Адрес')),
                ('notes', models.TextField(blank=True, max_length=200, verbose_name='Примечания к заказу')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('paid', models.BooleanField(default=False, verbose_name='Оплачен')),
                ('confirmed', models.BooleanField(default=False, verbose_name='Подтвержден')),
                ('send', models.BooleanField(default=False, verbose_name='Заказ отправлен')),
                ('date_send', models.DateField(blank=True, default=None, null=True, verbose_name='Дата отправления')),
                ('part', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='part_order', to='potlucks.part', verbose_name='Доля')),
            ],
            options={
                'verbose_name': 'Заказ доли пользователя в складчине',
                'verbose_name_plural': 'Заказы долей пользователей в складчинах',
            },
        ),
    ]
