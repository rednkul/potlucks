# Generated by Django 3.2.9 on 2022-07-20 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_remove_profile_instagram'),
        ('goods', '0002_auto_20220720_1443'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingStar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField(default=0, verbose_name='Значение')),
            ],
            options={
                'verbose_name': 'Звезда рейтинга',
                'verbose_name_plural': 'Звезды рейтинга',
                'ordering': ['-value'],
            },
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to='users.profile', verbose_name='Клиент')),
                ('products', models.ManyToManyField(blank=True, to='goods.Product', verbose_name='Товары')),
            ],
            options={
                'verbose_name': 'Отложенный товар',
                'verbose_name_plural': 'Отложенные товары',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, default='', max_length=5000, verbose_name='Отзыв о продукте')),
                ('date', models.DateField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile', verbose_name='Заказчик')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.product', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile', verbose_name='Заказчик')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.product', verbose_name='Заказ')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.ratingstar', verbose_name='Звезда рейтинга')),
            ],
            options={
                'verbose_name': 'Рейтинг',
                'verbose_name_plural': 'Рейтинги',
            },
        ),
    ]
