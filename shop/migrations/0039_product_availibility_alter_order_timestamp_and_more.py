# Generated by Django 4.1 on 2022-10-21 07:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0038_product_proccessor_alter_order_timestamp_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='availibility',
            field=models.CharField(choices=[('In Stock', 'In Stock'), ('Not In Stock', 'Not In Stock')], default='In Stock', max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 21, 7, 53, 49, 537455)),
        ),
        migrations.AlterField(
            model_name='orderupdate',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 21, 7, 53, 49, 537729)),
        ),
    ]
