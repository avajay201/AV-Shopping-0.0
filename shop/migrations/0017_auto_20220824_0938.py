# Generated by Django 2.2.6 on 2022-08-24 09:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_auto_20220823_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address_line1',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='address_line2',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 24, 9, 38, 24, 372570)),
        ),
        migrations.AlterField(
            model_name='orderupdate',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 24, 9, 38, 24, 372956)),
        ),
    ]
