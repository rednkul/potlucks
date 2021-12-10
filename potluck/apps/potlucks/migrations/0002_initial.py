# Generated by Django 3.2.6 on 2021-11-11 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('potlucks', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_reviews', to='users.profile', verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='reviews',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_reviews', to='potlucks.order', verbose_name='Заказ'),
        ),
        migrations.AddField(
            model_name='rating',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_ratings', to='users.profile', verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='rating',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_ratings', to='users.profile', verbose_name='Заказ'),
        ),
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='product_categories', to='potlucks.Category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='product',
            name='manufacturer',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='manufacturer_products', to='potlucks.vendor', verbose_name='Производитель'),
        ),
        migrations.AddField(
            model_name='product',
            name='vendors',
            field=models.ManyToManyField(related_name='product_vendors', to='potlucks.Vendor', verbose_name='Поставщики'),
        ),
        migrations.AddField(
            model_name='order',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_creators', to='users.profile', verbose_name='Создатель'),
        ),
        migrations.AddField(
            model_name='order',
            name='partners',
            field=models.ManyToManyField(related_name='order_partners', to='users.Profile', verbose_name='Участники'),
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_orders', to='potlucks.product', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='order',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_vendor', to='potlucks.vendor', verbose_name='Поставщик'),
        ),
        migrations.AddField(
            model_name='customerorder',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile', verbose_name='Участник заказа'),
        ),
        migrations.AddField(
            model_name='customerorder',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='potlucks.order', verbose_name='Заказ'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='potlucks.category', verbose_name='Родитель'),
        ),
    ]
