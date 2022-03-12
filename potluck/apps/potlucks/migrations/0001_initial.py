# Generated by Django 3.2.9 on 2022-02-15 15:22

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0011_rename_patrynomic_profile_patronymic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Категория')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(blank=True, upload_to='categories/', verbose_name='Изображение')),
                ('url', models.SlugField(max_length=160)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subcategories', to='potlucks.category', verbose_name='Родитель')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='CustomerOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_number', models.PositiveSmallIntegerField(default=0, verbose_name='Доля пользователя в заказе')),
                ('address', models.CharField(blank=True, max_length=100, verbose_name='Адрес доставки')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Время присоединения к заказу')),
                ('paid', models.BooleanField(default=False, verbose_name='Доля пользователя в заказе оплачена')),
                ('send', models.BooleanField(default=False, verbose_name='Заказ отправлен')),
                ('notes', models.TextField(blank=True, max_length=300, verbose_name='Примечание к заказу')),
                ('date_send', models.DateField(blank=True, default=None, null=True, verbose_name='Дата отправления')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile', verbose_name='Участник заказа')),
            ],
            options={
                'verbose_name': 'Заказ пользователя',
                'verbose_name_plural': 'Заказы пользователей',
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Наименование')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(blank=True, upload_to='manufacturers/', verbose_name='Логотип')),
                ('url', models.SlugField(max_length=160, unique=True)),
            ],
            options={
                'verbose_name': 'Производитель',
                'verbose_name_plural': 'Производители',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sizes_eu', models.CharField(blank=True, max_length=10, verbose_name='Линейка европейских размеров')),
                ('sizes_am', models.CharField(blank=True, max_length=15, verbose_name='Линейка американских размеров')),
                ('colors', models.CharField(blank=True, max_length=40, verbose_name='Линейка цветов')),
                ('materials', models.CharField(blank=True, max_length=40, verbose_name='Материалы')),
                ('name', models.CharField(max_length=50, verbose_name='Наименование товара')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(blank=True, upload_to='products/', verbose_name='Изображение')),
                ('url', models.SlugField(max_length=160, unique=True)),
                ('tags', models.TextField(blank=True, max_length=200, verbose_name='Тэги товара')),
                ('category', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_products', to='potlucks.category', verbose_name='Категория')),
                ('manufacturer', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='manufacturer_products', to='potlucks.manufacturer', verbose_name='Производитель')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
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
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Наименование')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(blank=True, upload_to='vendors/', verbose_name='Логотип')),
                ('finished_orders', models.PositiveSmallIntegerField(default=0, verbose_name='Завершенные заказы')),
                ('contact_phone', models.CharField(blank=True, max_length=12, verbose_name='Номер телефона')),
                ('contact_site', models.CharField(blank=True, max_length=50, verbose_name='Сайт')),
                ('contact_social', models.CharField(blank=True, max_length=200, verbose_name='Социальные сети')),
                ('url', models.SlugField(max_length=160)),
            ],
            options={
                'verbose_name': 'Поставщик',
                'verbose_name_plural': 'Поставщики',
            },
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to='users.profile', verbose_name='Клиент')),
                ('products', models.ManyToManyField(blank=True, to='potlucks.Product', verbose_name='Товары')),
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
                ('customer_order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='potlucks.customerorder', verbose_name='Заказ')),
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
                ('customer_order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='potlucks.customerorder', verbose_name='Заказ')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='potlucks.ratingstar', verbose_name='Звезда рейтинга')),
            ],
            options={
                'verbose_name': 'Рейтинг',
                'verbose_name_plural': 'Рейтинги',
            },
        ),
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product/product_images', verbose_name='Изображение товара')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='potlucks.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Дополнительное изображение товара',
                'verbose_name_plural': 'Дополнительные изображения товара',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='vendors',
            field=models.ManyToManyField(related_name='vendor_products', to='potlucks.Vendor', verbose_name='Поставщики'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.PositiveSmallIntegerField(default=0, verbose_name='Количество единиц товара в заказе')),
                ('unit_price', models.PositiveIntegerField(default=0, help_text='Сумма в рублях', verbose_name='Цена за единицу товара')),
                ('price', models.PositiveIntegerField(default=0, help_text='Сумма в рублях', verbose_name='Стоимость заказа')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('date_amass', models.DateTimeField(blank=True, null=True, verbose_name='Время заполнения')),
                ('url', models.SlugField(max_length=160, unique=True)),
                ('number_finished', models.PositiveSmallIntegerField(default=0, verbose_name='Завершено заказов такого же товара в таком же количестве')),
                ('amassed', models.BooleanField(default=False, verbose_name='Все позиции заказа забронированы')),
                ('paid', models.BooleanField(default=False, verbose_name='Заказ полностью оплачен')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_creators', to='users.profile', verbose_name='Создатель')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_orders', to='potlucks.product', verbose_name='Товар')),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_vendor', to='potlucks.vendor', verbose_name='Поставщик')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='customerorder',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_reserved', to='potlucks.order', verbose_name='Заказ'),
        ),
        migrations.AlterUniqueTogether(
            name='customerorder',
            unique_together={('order', 'customer')},
        ),
    ]
