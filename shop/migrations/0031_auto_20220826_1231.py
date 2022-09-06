# Generated by Django 2.2.6 on 2022-08-26 12:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0030_auto_20220826_0821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 26, 12, 31, 6, 916525)),
        ),
        migrations.AlterField(
            model_name='orderupdate',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 26, 12, 31, 6, 916991)),
        ),
        migrations.AlterField(
            model_name='orderupdate',
            name='update_desc',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]