# Generated by Django 4.2.4 on 2023-11-20 06:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_products_ratings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='ratings',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)]),
        ),
    ]
