# Generated by Django 4.0.5 on 2022-07-11 10:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets_management', '0007_alter_systemhostedapplication_usage_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atm',
            name='recorded_date',
            field=models.DateTimeField(db_column='recorded_date', default=datetime.datetime(2022, 7, 11, 12, 2, 36, 577189), verbose_name='Recorded date'),
        ),
        migrations.AlterField(
            model_name='biovayanotecountergenerator',
            name='recorded_date',
            field=models.DateTimeField(db_column='recorded_date', default=datetime.datetime(2022, 7, 11, 12, 2, 36, 577189), verbose_name='Recorded date'),
        ),
        migrations.AlterField(
            model_name='computerlapdesktop',
            name='recorded_date',
            field=models.DateTimeField(db_column='recorded_date', default=datetime.datetime(2022, 7, 11, 12, 2, 36, 577189), verbose_name='Recorded date'),
        ),
        migrations.AlterField(
            model_name='physicalnode',
            name='recorded_date',
            field=models.DateTimeField(db_column='recorded_date', default=datetime.datetime(2022, 7, 11, 12, 2, 36, 577189), verbose_name='Recorded date'),
        ),
        migrations.AlterField(
            model_name='printerscanner',
            name='recorded_date',
            field=models.DateTimeField(db_column='recorded_date', default=datetime.datetime(2022, 7, 11, 12, 2, 36, 577189), verbose_name='Recorded date'),
        ),
        migrations.AlterField(
            model_name='screen',
            name='recorded_date',
            field=models.DateTimeField(db_column='recorded_date', default=datetime.datetime(2022, 7, 11, 12, 2, 36, 577189), verbose_name='Recorded date'),
        ),
        migrations.AlterField(
            model_name='switchrouterfirewall',
            name='recorded_date',
            field=models.DateTimeField(db_column='recorded_date', default=datetime.datetime(2022, 7, 11, 12, 2, 36, 577189), verbose_name='Recorded date'),
        ),
        migrations.AlterField(
            model_name='systemhostedapplication',
            name='recorded_date',
            field=models.DateTimeField(db_column='recorded_date', default=datetime.datetime(2022, 7, 11, 12, 2, 36, 581189), verbose_name='Recorded date'),
        ),
    ]
