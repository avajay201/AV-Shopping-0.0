# Generated by Django 2.2.6 on 2022-08-23 10:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20220823_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 23, 10, 17, 6, 684135)),
        ),
        migrations.AlterField(
            model_name='orderupdate',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 23, 10, 17, 6, 684552)),
        ),
    ]
