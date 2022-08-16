# Generated by Django 4.0.6 on 2022-08-05 07:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atm',
            name='recorded_date',
            field=models.DateTimeField(db_column='recorded_date', default=datetime.datetime(2022, 8, 5, 9, 45, 41, 986557), verbose_name='Recorded date'),
        ),
        migrations.AlterField(
            model_name='biovayanotecountergenerator',
            name='recorded_date',
            field=models.DateTimeField(db_column='recorded_date', default=datetime.datetime(2022, 8, 5, 9, 45, 41, 986557), verbose_name='Recorded date'),
        ),
        migrations.AlterField(
            model_name='computerlapdesktop',
            name='recorded_date',
            field=models.DateTimeField(db_column='recorded_date', default=datetime.datetime(2022, 8, 5, 9, 45, 41, 986557), verbose_name='Recorded date'),
        ),
        migrations.AlterField(
            model_name='physicalnode',
            name='recorded_date',
            field=models.DateTimeField(db_column='recorded_date', default=datetime.datetime(2022, 8, 5, 9, 45, 41, 986557), verbose_name='Recorded date'),
        ),
        migrations.AlterField(
            model_name='printerscanner',
            name='recorded_date',
            field=models.DateTimeField(db_column='recorded_date', default=datetime.datetime(2022, 8, 5, 9, 45, 41, 986557), verbose_name='Recorded date'),
        ),
        migrations.AlterField(
            model_name='screen',
            name='recorded_date',
            field=models.DateTimeField(db_column='recorded_date', default=datetime.datetime(2022, 8, 5, 9, 45, 41, 986557), verbose_name='Recorded date'),
        ),
        migrations.AlterField(
            model_name='switchrouterfirewall',
            name='recorded_date',
            field=models.DateTimeField(db_column='recorded_date', default=datetime.datetime(2022, 8, 5, 9, 45, 41, 986557), verbose_name='Recorded date'),
        ),
        migrations.AlterField(
            model_name='systemhostedapplication',
            name='recorded_date',
            field=models.DateTimeField(db_column='recorded_date', default=datetime.datetime(2022, 8, 5, 9, 45, 41, 986557), verbose_name='Recorded date'),
        ),
    ]