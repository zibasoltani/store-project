# Generated by Django 5.1.1 on 2024-09-23 16:33

import jalali_date_new.model_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_alter_cart_created_at_alter_cart_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='created_at',
            field=jalali_date_new.model_fields.JalaliDateTimeModelField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='updated_at',
            field=jalali_date_new.model_fields.JalaliDateTimeModelField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='price',
            field=jalali_date_new.model_fields.JalaliDateTimeModelField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=jalali_date_new.model_fields.JalaliDateTimeModelField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=jalali_date_new.model_fields.JalaliDateTimeModelField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='updated_at',
            field=jalali_date_new.model_fields.JalaliDateTimeModelField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=jalali_date_new.model_fields.JalaliDateTimeModelField(),
        ),
    ]