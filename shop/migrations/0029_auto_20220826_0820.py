# Generated by Django 2.2.6 on 2022-08-26 08:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0028_auto_20220826_0807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 26, 8, 20, 52, 197270)),
        ),
        migrations.AlterField(
            model_name='orderupdate',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 26, 8, 20, 52, 197722)),
        ),
        migrations.AlterField(
            model_name='orderupdate',
            name='update_desc',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
