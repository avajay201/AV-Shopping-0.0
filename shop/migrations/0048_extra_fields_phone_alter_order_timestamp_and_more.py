# Generated by Django 4.1 on 2022-10-28 06:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0047_alter_order_timestamp_alter_orderupdate_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='extra_fields',
            name='phone',
            field=models.CharField(default='', max_length=13),
        ),
        migrations.AlterField(
            model_name='order',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 28, 6, 54, 53, 305573)),
        ),
        migrations.AlterField(
            model_name='orderupdate',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 28, 6, 54, 53, 305837)),
        ),
    ]
