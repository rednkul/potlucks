# Generated by Django 3.2.9 on 2022-07-08 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('potlucks', '0006_parameters_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameters',
            name='type',
            field=models.CharField(choices=[('number', 'Число'), ('text', 'Текст')], default='text', help_text='Для числового параметра (например, размер, кол-во чего-либо) - число, для остальных - текст.', max_length=6, verbose_name='Тип параметра'),
        ),
    ]
