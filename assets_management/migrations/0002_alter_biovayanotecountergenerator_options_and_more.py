# Generated by Django 4.0.5 on 2022-07-03 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='biovayanotecountergenerator',
            options={'verbose_name': 'biometric/avaya/note counter/generator', 'verbose_name_plural': 'biometrics/avaya/note_counters/generators'},
        ),
        migrations.AlterModelOptions(
            name='computerlapdesktop',
            options={'verbose_name': 'computer', 'verbose_name_plural': 'computers'},
        ),
        migrations.AlterModelOptions(
            name='physicalnode',
            options={'verbose_name': 'physical server', 'verbose_name_plural': 'physical servers'},
        ),
        migrations.AlterModelOptions(
            name='printerscanner',
            options={'verbose_name': 'printer/scanner', 'verbose_name_plural': 'printers/scanners'},
        ),
        migrations.AlterModelOptions(
            name='switchrouterfirewall',
            options={'verbose_name': 'switch/router/firewall', 'verbose_name_plural': 'switches/routers/firewalls'},
        ),
        migrations.AlterModelOptions(
            name='systemhostedapplication',
            options={'verbose_name': 'system hosted application', 'verbose_name_plural': 'system hosted applications'},
        ),
        migrations.AlterField(
            model_name='atm',
            name='status',
            field=models.CharField(choices=[('WORKING-GOOD', 'WORKING GOOD'), ('WORKING-BAD', 'WORKING BAD'), ('NOT-WORKING', 'NOT WORKING'), ('NEW', 'NEW')], db_column='status', max_length=15, verbose_name='Working status'),
        ),
        migrations.AlterField(
            model_name='atm',
            name='which_store',
            field=models.CharField(choices=[('PROCUREMENT', 'Procurement'), ('IT', 'IT'), ('MUHANGA-DR', 'Muhanga DR'), ('NOT-IN-STORE', 'Not in store')], db_column='which_store', max_length=20, verbose_name='Which store'),
        ),
        migrations.AlterField(
            model_name='biovayanotecountergenerator',
            name='status',
            field=models.CharField(choices=[('WORKING-GOOD', 'WORKING GOOD'), ('WORKING-BAD', 'WORKING BAD'), ('NOT-WORKING', 'NOT WORKING'), ('NEW', 'NEW')], db_column='status', max_length=15, verbose_name='Working status'),
        ),
        migrations.AlterField(
            model_name='biovayanotecountergenerator',
            name='which_store',
            field=models.CharField(choices=[('PROCUREMENT', 'Procurement'), ('IT', 'IT'), ('MUHANGA-DR', 'Muhanga DR'), ('NOT-IN-STORE', 'Not in store')], db_column='which_store', max_length=20, verbose_name='Which store'),
        ),
        migrations.AlterField(
            model_name='computerlapdesktop',
            name='processor_type',
            field=models.CharField(choices=[('Single-Core', 'Single Core'), ('Dual-Core', 'Dual Core'), ('Quad-Core', 'Quad Core'), ('Hexa-Core', 'Hexa Core'), ('Octa-Core', 'Octa Core'), ('Deca Core', 'Deca Core')], db_column='processor_type', max_length=15, verbose_name='Processor type'),
        ),
        migrations.AlterField(
            model_name='computerlapdesktop',
            name='status',
            field=models.CharField(choices=[('WORKING-GOOD', 'WORKING GOOD'), ('WORKING-BAD', 'WORKING BAD'), ('NOT-WORKING', 'NOT WORKING'), ('NEW', 'NEW')], db_column='status', max_length=15, verbose_name='Working status'),
        ),
        migrations.AlterField(
            model_name='computerlapdesktop',
            name='storage_type',
            field=models.CharField(choices=[('HARD-DISK', 'HARD DISK'), ('SSD', 'SSD'), ('HARD-DISK-+-SSD', 'HARD DISK + SSD')], db_column='storage_type', max_length=20, verbose_name='Storage type'),
        ),
        migrations.AlterField(
            model_name='computerlapdesktop',
            name='which_store',
            field=models.CharField(choices=[('PROCUREMENT', 'Procurement'), ('IT', 'IT'), ('MUHANGA-DR', 'Muhanga DR'), ('NOT-IN-STORE', 'Not in store')], db_column='which_store', max_length=20, verbose_name='Which store'),
        ),
        migrations.AlterField(
            model_name='physicalnode',
            name='status',
            field=models.CharField(choices=[('WORKING-GOOD', 'WORKING GOOD'), ('WORKING-BAD', 'WORKING BAD'), ('NOT-WORKING', 'NOT WORKING'), ('NEW', 'NEW')], db_column='status', max_length=15, verbose_name='Working status'),
        ),
        migrations.AlterField(
            model_name='physicalnode',
            name='which_store',
            field=models.CharField(choices=[('PROCUREMENT', 'Procurement'), ('IT', 'IT'), ('MUHANGA-DR', 'Muhanga DR'), ('NOT-IN-STORE', 'Not in store')], db_column='which_store', max_length=20, verbose_name='Which store'),
        ),
        migrations.AlterField(
            model_name='printerscanner',
            name='category_type',
            field=models.CharField(choices=[('STATEMENT-PRINTER', 'STATEMENT PRINTER'), ('CARD-PRINTER', 'CARD PRINTER'), ('CHEQUE-PRINTER', 'CHEQUE PRINTER'), ('PAPER-PRINTER', 'PAPER PRINTER'), ('CHEQUE-SCANNER', 'CHEQUE SCANNER'), ('ACCOUNT-OPENING SCANNER', 'ACCOUNT OPEN SCANNER'), ('OTHER', 'OTHER')], db_column='type', max_length=30, verbose_name='Printer/scanner type'),
        ),
        migrations.AlterField(
            model_name='printerscanner',
            name='status',
            field=models.CharField(choices=[('WORKING-GOOD', 'WORKING GOOD'), ('WORKING-BAD', 'WORKING BAD'), ('NOT-WORKING', 'NOT WORKING'), ('NEW', 'NEW')], db_column='status', max_length=15, verbose_name='Working status'),
        ),
        migrations.AlterField(
            model_name='printerscanner',
            name='which_store',
            field=models.CharField(choices=[('PROCUREMENT', 'Procurement'), ('IT', 'IT'), ('MUHANGA-DR', 'Muhanga DR'), ('NOT-IN-STORE', 'Not in store')], db_column='which_store', max_length=20, verbose_name='Which store'),
        ),
        migrations.AlterField(
            model_name='screen',
            name='status',
            field=models.CharField(choices=[('WORKING-GOOD', 'WORKING GOOD'), ('WORKING-BAD', 'WORKING BAD'), ('NOT-WORKING', 'NOT WORKING'), ('NEW', 'NEW')], db_column='status', max_length=15, verbose_name='Working status'),
        ),
        migrations.AlterField(
            model_name='screen',
            name='which_store',
            field=models.CharField(choices=[('PROCUREMENT', 'Procurement'), ('IT', 'IT'), ('MUHANGA-DR', 'Muhanga DR'), ('NOT-IN-STORE', 'Not in store')], db_column='which_store', max_length=20, verbose_name='Which store'),
        ),
        migrations.AlterField(
            model_name='switchrouterfirewall',
            name='status',
            field=models.CharField(choices=[('WORKING-GOOD', 'WORKING GOOD'), ('WORKING-BAD', 'WORKING BAD'), ('NOT-WORKING', 'NOT WORKING'), ('NEW', 'NEW')], db_column='status', max_length=15, verbose_name='Working status'),
        ),
        migrations.AlterField(
            model_name='switchrouterfirewall',
            name='which_store',
            field=models.CharField(choices=[('PROCUREMENT', 'Procurement'), ('IT', 'IT'), ('MUHANGA-DR', 'Muhanga DR'), ('NOT-IN-STORE', 'Not in store')], db_column='which_store', max_length=20, verbose_name='Which store'),
        ),
    ]
