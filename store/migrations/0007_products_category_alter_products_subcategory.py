# Generated by Django 4.2.4 on 2023-11-15 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_products_is_stock_products_stock_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='store.category'),
        ),
        migrations.AlterField(
            model_name='products',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.subcategory'),
        ),
    ]
