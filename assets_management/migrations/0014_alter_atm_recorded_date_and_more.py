# Generated by Django 4.0.5 on 2022-07-12 18:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets_management', '0013_alter_atm_recorded_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atm',
            name='recorded_date',
            field=models.DateTimeField(db_column='recorded_date', default=datetime.datetime(2022, 7, 12, 20, 58, 45, 865319), verbose_name='Recorded date'),
        ),
        migrations.AlterField(
            model_name='biovayanotecountergenerator',
            name='recorded_date',
            field=models.DateTimeField(db_column='recorded_date', default=datetime.datetime(2022, 7, 12, 20, 58, 45, 865319), verbose_name='Recorded date'),
        ),
        migrations.AlterField(
            model_name='computerlapdesktop',
            name='recorded_date',
            field=models.DateTimeField(db_column='recorded_date', default=datetime.datetime(2022, 7, 12, 20, 58, 45, 865319), verbose_name='Recorded date'),
        ),
        migrations.AlterField(
            model_name='physicalnode',
            name='recorded_date',
            field=models.DateTimeField(db_column='recorded_date', default=datetime.datetime(2022, 7, 12, 20, 58, 45, 865319), verbose_name='Recorded date'),
        ),
        migrations.AlterField(
            model_name='printerscanner',
            name='recorded_date',
            field=models.DateTimeField(db_column='recorded_date', default=datetime.datetime(2022, 7, 12, 20, 58, 45, 865319), verbose_name='Recorded date'),
        ),
        migrations.AlterField(
            model_name='screen',
            name='recorded_date',
            field=models.DateTimeField(db_column='recorded_date', default=datetime.datetime(2022, 7, 12, 20, 58, 45, 865319), verbose_name='Recorded date'),
        ),
        migrations.AlterField(
            model_name='switchrouterfirewall',
            name='recorded_date',
            field=models.DateTimeField(db_column='recorded_date', default=datetime.datetime(2022, 7, 12, 20, 58, 45, 865319), verbose_name='Recorded date'),
        ),
        migrations.AlterField(
            model_name='systemhostedapplication',
            name='recorded_date',
            field=models.DateTimeField(db_column='recorded_date', default=datetime.datetime(2022, 7, 12, 20, 58, 45, 867379), verbose_name='Recorded date'),
        ),
    ]
