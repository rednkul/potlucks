# Generated by Django 3.2.9 on 2022-07-20 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
        ('retail', '0014_auto_20220719_1344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimages',
            name='product',
        ),
        migrations.RemoveField(
            model_name='producttoretail',
            name='category',
        ),
        migrations.RemoveField(
            model_name='producttoretail',
            name='manufacturer',
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='goods.product', verbose_name='Товар'),
        ),
        migrations.DeleteModel(
            name='CategoryToRetail',
        ),
        migrations.DeleteModel(
            name='ProductImages',
        ),
        migrations.DeleteModel(
            name='ProductToRetail',
        ),
    ]
