# Generated by Django 5.1.1 on 2024-09-24 07:35

import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_alter_order_total_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='updated_at',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
    ]
