from django.db import models
from assets_management.models import ComputerLapDeskTop, PrinterScanner, Atm,BioVayaNoteCounterGenerator


class MaintenanceLog(models.Model):
    TYPES = (
        ("PREVENTIVE_MAINTENANCE", "PREVENTIVE_MAINTENANCE"),
        ("UNEXPECTED_MAINTENANCE", "UNEXPECTED_MAINTENANCE")
    )

    ASSET_MAINTENANCE_CATEGORY = (
        ("COMPUTER_MAINTENANCE", "COMPUTER_MAINTENANCE"),
        ("PRINTER_MAINTENANCE", "PRINTER_MAINTENANCE"),
        ("SCANNER_MAINTENANCE", "SCANNER_MAINTENANCE"),
        ("ATM_MAINTENANCE", "ATM_MAINTENANCE"),
        ("NOTE_COUNTER_MAINTENANCE", "NOTE_COUNTER_MAINTENANCE")
    )

    maintenance_type = models.CharField("Maintenance type", blank=False, null=False, db_column="maintenance_type", max_length=30, choices=TYPES)
    maintenance_asset_category = models.CharField("Maintenance asset category", blank=False, null=False, db_column="maintenance_asset_category", max_length=30, choices=ASSET_MAINTENANCE_CATEGORY)
    ticket_type = models.CharField("Ticket type", max_length=250, blank=False, null=False, db_column="ticket_type")
    environment_check = models.TextField("Environment check", blank=False, null=False, db_column="environment_check")
    areas_serviced = models.CharField("Areas serviced", max_length=250, blank=False, null=False, db_column="areas_serviced")
    additional_note = models.TextField("Additional note", blank=True, null=True, db_column="description")
    maintenance_cost = models.DecimalField("Maintenance cost", decimal_places=2, max_digits=12, db_column="maintenance_cost")
    spareparts_quantity_used = models.PositiveIntegerField("Sparepart quantity used", db_column="sparepart_quantity_used", blank=False, null=False)
    start_date = models.DateField("Start date", blank=False, null=False, db_column="start_date")
    end_date = models.DateField("End date", blank=False, null=False, db_column="end_start")
    computer = models.ForeignKey(ComputerLapDeskTop, verbose_name="Computer", on_delete=models.CASCADE, db_column="computer_id", related_name="computer_logs", null=True, blank=True)
    printer_scanner = models.ForeignKey(PrinterScanner, verbose_name="Printer/Scanner", on_delete=models.CASCADE, db_column="printer_scanner_id", related_name="printer_scanner_logs", null=True, blank=True)
    atm = models.ForeignKey(Atm, verbose_name="ATM", on_delete=models.CASCADE, db_column="atm_id", related_name="atm_logs", null=True, blank=True)
    note_counter = models.ForeignKey(BioVayaNoteCounterGenerator, verbose_name="Note counter", on_delete=models.CASCADE, db_column="note_counter_id", related_name="note_counter_logs", null=True, blank=True)
    
    class Meta:
        db_table = "maintenance_logs"

    def __str__(self) -> str:
        return f"{self.maintenance_type}"



class SparePart(models.Model):
    SPAREPARTS_CATEGORIES = (
        ("COMPUTER_SPAREPART", "COMPUTER_SPAREPART"),
        ("PRINTER_SCANNER_SPAREPART", "PRINTER_SCANNER_SPAREPART"),
        ("ATM_SPAREPART", "ATM_SPAREPART"),
        ("NOTE_COUNTER_SPAREPART", "NOTE_COUNTER_SPAREPART"),
    )

    sparepart_category = models.CharField("Sparepart category", max_length=40, blank=False, null=False, db_column="sparepart_category", choices=SPAREPARTS_CATEGORIES)
    serial_number = models.CharField("Serial number", max_length=40, blank=False, null=False, db_column="serial_number", unique=True)
    sparepart_name = models.CharField("Sparepart name", max_length=50, blank=False, null=False, db_column="sparepart_name")
    unit_price = models.DecimalField("Unit price", decimal_places=2, max_digits=10, blank=False, null=False, db_column="unit_price")
    delivery_date = models.DateField("Delivery date", blank=False, null=False, db_column="delivery_date")
    was_used = models.BooleanField("Was used", db_column="was_used", default=False)
    maintenance_log = models.ForeignKey(MaintenanceLog, verbose_name="Maintenance Log", db_column="maintenance_log_id", on_delete=models.CASCADE, related_name="spareparts_used", null=True, blank=True)    


    class Meta:
        db_table = "spareparts"
    
    def __str__(self) -> str:
        return f"{self.sparepart_name}"