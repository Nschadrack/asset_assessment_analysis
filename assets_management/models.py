from datetime import datetime

from django.db import models



class CommonAsset(models.Model):
    """
     This is an abstract model which contains common attributes to be inherited
     by other models
    """
    STORES = (
        ('Procurement', 'Procurement'),
        ('IT', 'IT'),
        ('Muhanga DR', 'Muhanga DR'),
        ('Not in store', 'Not in store')
    )
    STATUES = (
        ('WORKING GOOD', 'WORKING GOOD'),
        ('WORKING BAD', 'WORKING BAD'),
        ('NOT WORKING', 'NOT WORKING'),
        ('NEW', 'NEW')
    )

    asset_id = models.BigAutoField(verbose_name='Asset id', primary_key=True, db_column='asset_id', null=False, blank=False)
    serial_number = models.CharField(verbose_name='Serial number', max_length=40, db_column='serial_number', null=False, blank=False, unique=True,
                                    error_messages={'unique': 'Computer with serial number is already exists'})
    model = models.CharField(verbose_name='Model', max_length=100, db_column='model', null=False, blank=False)
    tag_number = models.CharField(verbose_name='Tag number', max_length=40, db_column='tag_number', null=True, blank=True, unique=True,
                                error_messages={'unique': 'Computer with tag number is already exists'})
    purchase_price = models.PositiveIntegerField(verbose_name='Purchase price', db_column='purchase_price', null=False, blank=False)
    recorded_date = models.DateTimeField(verbose_name='Recorded date', db_column='recorded_date', null=False, blank=False, auto_now_add=True)
    entry_date_in_bank = models.DateField(verbose_name='Entry date in bank', db_column='entry_date_in_bank', null=False, blank=False)
    usage_start_date = models.DateTimeField(verbose_name='Usage start date', db_column='usage_start_date', null=True, blank=True, editable=False)
    warranty_time = models.PositiveIntegerField(verbose_name='Warranty time in months', db_column='warranty_time', null=False, blank=False)
    lifetime = models.PositiveIntegerField(verbose_name='Lifetime in months', db_column='lifetime', null=False, blank=False)
    warranty_time_formated = models.CharField(verbose_name='Formatted Warranty time', max_length=60, db_column='formatted_warranty', null=False, 
                                                blank=False, editable=False)
    lifetime_formated = models.CharField(verbose_name='Formatted lifetime', max_length=60, db_column='formatted_lifetime', null=False, blank=False, 
                                                editable=False)
    in_store = models.BooleanField(verbose_name='In store', db_column='in_store', null=False, blank=False)
    which_store = models.CharField(verbose_name='Which store', max_length=20, db_column='which_store', null=False, blank=False, choices=STORES)
    asset_sold = models.BooleanField(verbose_name='Asset sold', db_column='asset_sold', default=False)
    sold_date = models.DateField(verbose_name='sold_date', db_column='sold_date', null=True, blank=True)
    sale_price = models.PositiveIntegerField(verbose_name='Sale price', db_column='sale_price', null=True, blank=True)
    in_use = models.BooleanField(verbose_name='In use', default=False, db_column='in_use')
    still_functions = models.BooleanField(verbose_name='Still functions', db_column='still_functions', default=True)
    status = models.CharField(verbose_name='Working status', max_length=15, db_column='status', default='NEW', choices=STATUES)
    

    class Meta:
        abstract = True

    @property
    def add_usage_start_date(self):
        self.usage_start_date = datetime.now()
        self.save()
    
    def set_status(self, new_status):
        self.status = new_status
        self.save()

    @property
    def set_warranty_time_formated(self):
        if self.warranty_time < 12:
            self.warranty_time_formated = f"{self.warranty_time} months"
        else:
            remaining_months = self.warranty_time % 12
            if int(self.warranty_time / 12) > 1:
                    years = f"{int(self.warranty_time /12)} years"
            else:
                years = f"{int(self.warranty_time /12)} year"

            if remaining_months > 0:
                if self.warranty_time % 12  > 1:
                    months = f"{self.warranty_time % 12} months"
                else:
                    months = f"{self.warranty_time % 12} month"                
                self.warranty_time_formated = f"{years} {months}"
            else:
                self.warranty_time_formated = years
    

    @property
    def set_lifetime_formated(self):
        if self.lifetime < 12:
            self.lifetime_formated =  f"{self.lifetime} months"
        else:
            remaining_months = self.lifetime % 12
            if int(self.lifetime / 12) > 1:
                years = f"{int(self.lifetime /12)} years"
            else:
                years = f"{int(self.lifetime /12)} year"

            if remaining_months > 0:
                if self.lifetime % 12 > 1:
                    months = f"{self.lifetime % 12} months"
                else:
                    months = f"{self.lifetime % 12} month"
                self.lifetime_formated = f"{years} {months}"
            else:
                self.lifetime_formated =  years
    

    def save(self, *args, **kwargs):
        self.set_warranty_time_formated
        self.set_lifetime_formated
        super().save(*args, **kwargs)


########################## Computers model #############################################################################################
class ComputerLapDeskTop(CommonAsset):
    """
    The model for Computers asset category which inherits CommonAsset abstract model
    """
    CATEGORIES = (
        ('LAPTOP', 'LAPTOP'),
        ('DESKTOP', 'DESKTOP')
    )
    STORAGE_TYPES = (
        ('HARD DISK', 'HARD DISK'),
        ('SSD', 'SSD'),
        ('HARD DISK + SSD', 'HARD DISK + SSD')
    )
    MEASUREMENTS = (
        ('MB', 'MB'),
        ('GB', 'GB'),
        ('TB', 'TB')
    )
    PROCESSOR_MANUFACTURES= (
        ('INTEL', 'INTEL'),
        ('AMD', 'AMD'),
        ('OTHER', 'OTHER')
    )
    PROCESSOR_TYPES = (
        ('Single Core', 'Single Core'),
        ('Dual Core', 'Dual Core'),
        ('Quad Core', 'Quad Core'),
        ('Hexa Core', 'Hexa Core'),
        ('Octa Core', 'Octa Core'),
        ('Deca Core', 'Deca Core')
    )
    PROCESSOR_SPEED_MEASUREMENTS = (
        ('MHz', 'MHz'),
        ('GHz', 'GHz')
    )
    hostname = models.CharField(verbose_name="Hostname", max_length=40, db_column='hostname', null=False, blank=False, unique=True,
                                error_messages={
                                    'unique': 'Computer with hostname is already exists'})
    category = models.CharField(verbose_name='Category', max_length=15, db_column='category', null=False, blank=False, choices=CATEGORIES)
    storage_type = models.CharField(verbose_name='Storage type', max_length=20, db_column='storage_type', null=False, blank=False, choices=STORAGE_TYPES)
    harddisk_size = models.PositiveIntegerField(verbose_name='Hard disk storage size', default=0, db_column='harddisk_size')
    ssd_size = models.PositiveBigIntegerField(verbose_name='SSD Size', db_column='ssd_size', default=0)
    harddisk_measure = models.CharField(verbose_name='Harddisk Measurement', max_length=6 ,db_column='harddisk_measure', choices=MEASUREMENTS, default='GB')
    ssd_measure = models.CharField(verbose_name='SSD Measurement', max_length=6, db_column='ssd_measure', choices=MEASUREMENTS, default='GB')
    memory_size = models.PositiveIntegerField(verbose_name='Memory size', db_column='memory_size', null=False, blank=False)
    memory_measure = models.CharField(verbose_name='Memory Measurement', max_length=6, db_column='memory_measure', choices=MEASUREMENTS, default='GB')
    processor_manufacturer = models.CharField(verbose_name='Processor manufacturer', max_length=10, db_column='processor_manufacturer', null=False, blank=False, 
                                                choices=PROCESSOR_MANUFACTURES)
    processor_type = models.CharField(verbose_name='Processor type', max_length=15, db_column='processor_type', null=False, blank=False, choices=PROCESSOR_TYPES)
    process_speed = models.DecimalField(verbose_name='Processor speed', decimal_places=2, max_digits=10, db_column='proccessor_speed', null=False, blank=False)
    processor_speed_measure = models.CharField(verbose_name='Processor speed measure', max_length=10, db_column='processor_measure', null=False, blank=False, 
                                               choices=PROCESSOR_SPEED_MEASUREMENTS, default='GHZ')
    processor_name = models.CharField(verbose_name='Processor name', max_length=40, db_column='processor_name', null=False, blank=False)
    symantic_installed = models.BooleanField('Symantic installed', db_column='symantic_installed', default=False)
    os_installed = models.CharField(verbose_name='OS Installed', max_length=60, db_column='os_installed', null=False, blank=False)

    class Meta:
        db_table = 'computers'
        
    def __str__(self) -> str:
        return f"{self.category} : {self.hostname}"
    
    def set_symantic_installed(self, value):
        if value.upper() == "YES":
            self.symantic_installed = True 
        elif value.upper() == "NO":
            self.symantic_installed = False 
        self.save()

############################################# Printers and scanners ########################################
class PrinterScanner(CommonAsset):
    """
    The model for printers and scanners inherits CommonAsset model
    """
    CATEGORIES = (
        ('PRINTER', 'PRINTER'),
        ('SCANNER', 'SCANNER')
    )
    CATEGORY_TYPES = (
        ('STATEMENT PRINTER', 'STATEMENT PRINTER'),
        ('CARD PRINTER', 'CARD PRINTER'),
        ('CHEQUE PRINTER', 'CHEQUE PRINTER'),
        ('PAPER PRINTER', 'PAPER PRINTER'),
        ('CHEQUE SCANNER', 'CHEQUE SCANNER'),
        ('ACCOUNT OPENING SCANNER', 'ACCOUNT OPEN SCANNER'),
        ('OTHER', 'OTHER')
    )
    CONNECTION_TYPES = (
        ('USB', 'USB'),
        ('PARALLEL', 'PARALLEL'),
        ('SERIAL', 'SERIAL'),
        ('OTHER', 'OTHER'),
        ('NETWORK', 'NETWORK')
    )
    category = models.CharField(verbose_name='category', max_length=10, db_column='category', null=False, blank=False, choices=CATEGORIES)
    category_type = models.CharField(verbose_name='Printer/scanner type', max_length=30, db_column='type', null=False, blank=False, choices=CATEGORY_TYPES)
    other_type_name = models.CharField(verbose_name='Other type name', max_length=40, db_column='other_type_name', null=True, blank=True)
    connection_type = models.CharField(verbose_name='Connection type', max_length=20, db_column='connection_type', null=False, blank=False, choices=CONNECTION_TYPES)
    host_ip = models.CharField(verbose_name='Host IP', max_length=20, db_column='host_ip', null=True, blank=True, unique=True, 
                                error_messages={'unique': 'Printer or Scanner with host IP is already exists'})
    version = models.CharField(verbose_name='Version', max_length=15, db_column='version', null=True, blank=True)

    class Meta:
        db_table = 'printers_scanners'
    
    def __str__(self) -> str:
        return f"{self.category} : {self.category_type}"



############################################# Screen model ######################################################################################
class Screen(CommonAsset):
    """
    The model for monitors and TVs inherits CommonAsset
    """
    CATEGORIES = (
        ('TV', 'TV'),
        ('MONITOR', 'MONITOR')
    )
    category = models.CharField(verbose_name='Category', max_length=15, db_column='category', null=False, blank=False, choices=CATEGORIES)
    size = models.PositiveIntegerField(verbose_name='Screen size in inches', db_column='screen_size', null=False, blank=False)
    size_measure = models.CharField('Screen size measure', max_length=10, db_column='size_measure', default='inches', editable=False)

    
    class Meta:
        db_table = 'screens'
    
    def __str__(self) -> str:
        return f"{self.category} : {self.size} {self.size_measure}"


######################################### Biometrics, Avaya, Note counters and Generators ###############################################################
class BioVayaNoteCounterGenerator(CommonAsset):
    """
    The model for Biometrics, Avayas, Note counters and Generators inherits CommonAsset
    """
    CATEGORIES = (
        ('BIO', 'BIO'),
        ('AVAYA', 'AVAYA'),
        ('NOTE COUNTER', 'NOTE COUNTER'),
        ('GENERATOR', 'GENERATOR')
    )
    category = models.CharField(verbose_name='Category', max_length=15, db_column='category', null=False, blank=False, choices=CATEGORIES)
    version = models.CharField(verbose_name='Version', max_length=15, db_column='version', null=True, blank=True)

    class Meta:
        db_table = 'bio_avaya_note_counter_generator'

    def __str__(self) -> str:
        return f"{self.category}"


########################################### ATMs ##################################################################################################
class Atm(CommonAsset):
    """
    The model for ATMs inherits CommonAsset
    """
    hostname = models.CharField(verbose_name='Hostname', max_length=40, db_column='hostname', null=False, blank=False)
    os_installed = models.CharField(verbose_name='OS Installed', max_length=60, db_column='os_installed', null=False, blank=False)
    host_ip = models.CharField(verbose_name='Host IP', max_length=20, db_column='host_ip', null=True, blank=True)
    version = models.CharField(verbose_name='Version', max_length=15, db_column='version', null=True, blank=True)

    def add_usage_start_date(self, date_passed_in):
        self.usage_start_date = date_passed_in
        self.save()

    class Meta:
        db_table = 'atms'
    
    def __str__(self) -> str:
        return f"ATM: {self.hostname}"


##################################### Switch, Router, and Firewall model##########################################################################
class SwitchRouterFirewall(CommonAsset):
    """
    The model for Switch, Router and Firewall which inherits CommonAsset
    """
    CATEGORIES = (
        ('SWITCH', 'SWITCH'),
        ('ROUTER', 'ROUTER'),
        ('FIREWALL', 'FIREWALL')
    )
    hostname = models.CharField(verbose_name='Hostname', max_length=40, db_column='hostname', null=False, blank=False)
    service_ip = models.CharField(verbose_name='Service IP', max_length=20, db_column='service_ip', null=False, blank=False, unique=True,
                                error_messages={'unique': 'Router or Switch or Firewall with service IP is already exists'})
    category = models.CharField(verbose_name='Category', max_length=15, db_column='category', null=False, blank=False, choices=CATEGORIES)
    manufacturer = models.CharField(verbose_name='Manufacturer', max_length=60, db_column='manufacturer', null=True, blank=True)
    version = models.CharField(verbose_name='Version', max_length=15, db_column='version', null=True, blank=True)

    class Meta:
        db_table = 'switch_router_firewall'
    
    def add_usage_start_date(self, date_passed_in):
        self.usage_start_date = date_passed_in
        self.save()
    
    def __str__(self) -> str:
        return f"{self.category} : {self.hostname}"


################################### Physical Nodes ###############################################################################################
class PhysicalNode(CommonAsset):
    """
    The model for Physical Node which inherits CommonAsset
    """
    hostname = models.CharField(verbose_name='Hostname', max_length=40, db_column='hostname', null=False, blank=False)
    service_ip = models.CharField(verbose_name='Service IP', max_length=20, db_column='service_ip', null=False, blank=False)
    vendor = models.CharField(verbose_name='Vendor', max_length=60, db_column='vendor', null=False, blank=False)
    role = models.CharField(verbose_name='Role', max_length=40, db_column='role', null=True, blank=True)
    os_installed = models.CharField(verbose_name='Os Installed', max_length=100, db_column='os_installed', null=False, blank=False)
    installation_year = models.PositiveIntegerField(verbose_name='Year of installation', null=False, blank=False)

    class Meta:
        db_table = 'physical_nodes'
   
    def add_usage_start_date(self, date_passed_in):
        self.usage_start_date = date_passed_in
        self.save()
    
    def __str__(self) -> str:
        return f"{self.hostname}"


########################################## System hosted and application Model #######################################################################################
class SystemHostedApplication(models.Model):
    """
    The model for dealing with System hosted and applications
    """
    asset_id = models.BigAutoField(verbose_name='Asset id', primary_key=True, db_column='asset_id', null=False, blank=False)
    serial_number = models.CharField(verbose_name='Serial number', max_length=60, db_column='serial_number', null=False, blank=False, unique=True,
                                    error_messages={'unique': 'System host or application with serial number is already exists'})
    model = models.CharField(verbose_name='Model', max_length=100, db_column='model', null=False, blank=False)
    recorded_date = models.DateTimeField(verbose_name='Recorded date', db_column='recorded_date', null=False, blank=False, auto_now_add=True)
    usage_start_date = models.DateTimeField(verbose_name='Usage start date', db_column='usage_start_date', null=True, blank=True, editable=False)
    supporting_time = models.PositiveIntegerField(verbose_name='Supporting time in months', db_column='support_time', null=False, blank=False)
    supporting_time_formated = models.CharField(verbose_name='Formatted supporting time', max_length=60, db_column='formatted_support', null=False,
                                              blank=False, editable=False)
    in_use = models.BooleanField(verbose_name='In use', default=False, db_column='in_use')
    hostname = models.CharField(verbose_name='Hostname', max_length=40, db_column='hostname', null=False, blank=False)
    service_ip = models.CharField(verbose_name='Service IP', max_length=20, db_column='service_ip', null=False, blank=False)
    role = models.CharField(verbose_name='Role', max_length=40, db_column='role', null=True, blank=True)
    os_installed = models.CharField(verbose_name='Os Installed', max_length=100, db_column='os_installed', null=False, blank=False)
    installation_year = models.PositiveIntegerField(verbose_name='Year of installation', null=False, blank=False)

    class Meta:
        db_table = 'system_hosted_applications'

    def add_usage_start_date(self, date_passed_in):
        self.usage_start_date = date_passed_in
        self.save()

    @property
    def set_supporting_time_formated(self):
        if self.supporting_time < 12:
            self.supporting_time_formated = f"{self.supporting_time} months"
        else:
            remaining_months = self.supporting_time % 12
            if int(self.supporting_time / 12) > 1:
                years = f"{int(self.supporting_time /12)} years"
            else:
                years = f"{int(self.supporting_time /12)} year"

            if remaining_months > 0:
                if self.supporting_time % 12 > 1:
                    months = f"{self.supporting_time % 12} months"
                else:
                    months = f"{self.supporting_time % 12} month"
                self.supporting_time_formated = f"{years} {months}"
            else:
                self.supporting_time_formated = years


    def save(self, *args, **kwargs):
        self.set_supporting_time_formated
        super().save(*args, **kwargs)
