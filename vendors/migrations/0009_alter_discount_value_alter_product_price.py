# Generated by Django 5.1.1 on 2024-09-23 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0008_alter_product_created_at_alter_product_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='value',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
    ]
