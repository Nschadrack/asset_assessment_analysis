# Generated by Django 4.0.5 on 2022-07-17 08:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets_movement', '0009_alter_assetassignment_date_assigned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetassignment',
            name='date_assigned',
            field=models.DateTimeField(db_column='date_assigned', default=datetime.datetime(2022, 7, 17, 10, 52, 9, 725717), verbose_name='Date assigned'),
        ),
    ]
