# Generated by Django 5.1.1 on 2024-09-24 06:58

import jalali_date_new.model_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_alter_cartitem_price_alter_order_total_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=jalali_date_new.model_fields.JalaliDateTimeModelField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='updated_at',
            field=jalali_date_new.model_fields.JalaliDateTimeModelField(),
        ),
    ]
