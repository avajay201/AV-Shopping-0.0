# Generated by Django 4.1 on 2022-10-21 08:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0042_remove_product_images_alter_order_timestamp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 21, 8, 30, 39, 41047)),
        ),
        migrations.AlterField(
            model_name='orderupdate',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 21, 8, 30, 39, 41324)),
        ),
    ]
