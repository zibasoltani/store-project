# Generated by Django 5.1.1 on 2024-09-23 16:33

import jalali_date_new.model_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_review_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='created_at',
            field=jalali_date_new.model_fields.JalaliDateTimeModelField(auto_now=True),
        ),
    ]