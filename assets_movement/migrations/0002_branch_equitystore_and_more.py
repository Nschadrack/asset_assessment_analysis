# Generated by Django 4.0.5 on 2022-07-11 13:07

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets_movement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('code', models.PositiveIntegerField(db_column='code', primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(4000)], verbose_name='Branch code')),
                ('name', models.CharField(db_column='name', max_length=50, unique=True, verbose_name='Branch name')),
            ],
            options={
                'db_table': 'branches',
            },
        ),
        migrations.CreateModel(
            name='EquityStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', max_length=50, unique=True, verbose_name='Name')),
            ],
            options={
                'db_table': 'equity_stores',
            },
        ),
        migrations.AlterField(
            model_name='assetassignment',
            name='date_approved',
            field=models.DateTimeField(db_column='date_approved', default=datetime.datetime(2022, 7, 11, 15, 7, 52, 429190), verbose_name='Date approved/rejected'),
        ),
        migrations.AlterField(
            model_name='assetassignment',
            name='date_assigned',
            field=models.DateTimeField(db_column='date_assigned', default=datetime.datetime(2022, 7, 11, 15, 7, 52, 429190), verbose_name='Date assigned'),
        ),
    ]
