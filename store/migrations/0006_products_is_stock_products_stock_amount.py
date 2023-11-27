# Generated by Django 4.2.4 on 2023-11-15 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_subcategory_created_at_subcategory_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='is_stock',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='products',
            name='stock_amount',
            field=models.IntegerField(default=1),
        ),
    ]