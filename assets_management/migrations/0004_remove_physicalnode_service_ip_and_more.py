# Generated by Django 4.0.5 on 2022-07-05 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets_management', '0003_alter_atm_tag_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='physicalnode',
            name='service_ip',
        ),
        migrations.RemoveField(
            model_name='switchrouterfirewall',
            name='service_ip',
        ),
        migrations.RemoveField(
            model_name='systemhostedapplication',
            name='service_ip',
        ),
        migrations.AddField(
            model_name='physicalnode',
            name='host_ip',
            field=models.CharField(blank=True, db_column='host_ip', max_length=20, null=True, verbose_name='Host IP'),
        ),
        migrations.AddField(
            model_name='switchrouterfirewall',
            name='host_ip',
            field=models.CharField(blank=True, db_column='host_ip', max_length=20, null=True, verbose_name='Host IP'),
        ),
        migrations.AddField(
            model_name='systemhostedapplication',
            name='host_ip',
            field=models.CharField(blank=True, db_column='host_ip', max_length=20, null=True, verbose_name='Host IP'),
        ),
        migrations.AlterField(
            model_name='biovayanotecountergenerator',
            name='category',
            field=models.CharField(choices=[('BIO', 'BIO'), ('AVAYA', 'AVAYA'), ('NOTE-COUNTER', 'NOTE COUNTER'), ('GENERATOR', 'GENERATOR')], db_column='category', max_length=15, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='printerscanner',
            name='category_type',
            field=models.CharField(choices=[('STATEMENT-PRINTER', 'STATEMENT PRINTER'), ('CARD-PRINTER', 'CARD PRINTER'), ('CHEQUE-PRINTER', 'CHEQUE PRINTER'), ('PAPER-PRINTER', 'PAPER PRINTER'), ('CHEQUE-SCANNER', 'CHEQUE SCANNER'), ('ACCOUNT-OPENING-SCANNER', 'ACCOUNT OPEN SCANNER'), ('OTHER', 'OTHER')], db_column='type', max_length=30, verbose_name='Printer/scanner type'),
        ),
    ]