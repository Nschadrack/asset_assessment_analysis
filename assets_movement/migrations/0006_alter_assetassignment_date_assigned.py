# Generated by Django 4.0.5 on 2022-07-12 15:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets_movement', '0005_remove_assetassignment_siwtch_router_firewall_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetassignment',
            name='date_assigned',
            field=models.DateTimeField(db_column='date_assigned', default=datetime.datetime(2022, 7, 12, 17, 51, 35, 289371), verbose_name='Date assigned'),
        ),
    ]
