# Generated by Django 3.2.9 on 2022-08-14 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('PRIMARY', 'Основной'), ('SECONDARY', 'Дополнительный')], max_length=14, verbose_name='Назначение')),
                ('name', models.CharField(max_length=50, verbose_name='Наименование')),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('PRIMARY', 'Основной'), ('SECONDARY', 'Дополнительный')], max_length=14, verbose_name='Назначение')),
                ('email', models.EmailField(max_length=50, verbose_name='Наименование')),
            ],
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('PRIMARY', 'Основной'), ('SECONDARY', 'Дополнительный')], max_length=14, verbose_name='Назначение')),
                ('number', models.CharField(max_length=12, verbose_name='Номер')),
            ],
        ),
    ]