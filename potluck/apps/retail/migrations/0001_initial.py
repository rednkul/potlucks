# Generated by Django 3.2.9 on 2022-07-16 10:45

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryToRetail',
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
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subcategories', to='retail.categorytoretail', verbose_name='Родитель')),
            ],
            options={
                'verbose_name': 'Категория для розницы',
                'verbose_name_plural': 'Категории для розницы',
            },
        ),
        migrations.CreateModel(
            name='ProductToRetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Наименование товара')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(blank=True, upload_to='products/', verbose_name='Изображение')),
                ('url', models.SlugField(max_length=160, unique=True, verbose_name='URL')),
                ('tags', models.TextField(blank=True, max_length=200, verbose_name='Тэги товара')),
                ('available', models.BooleanField(default=True, verbose_name='Доступность')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Добавлен')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлён')),
                ('stock', models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Остаток')),
                ('price', models.PositiveIntegerField(default=0, help_text='Сумма в рублях', verbose_name='Стоимость')),
                ('category', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_products', to='retail.categorytoretail', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Товар для розницы',
                'verbose_name_plural': 'Товары для розницы',
            },
        ),
    ]