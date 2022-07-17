from django.db import models
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from users_management.models import User
from assets_management.models import (ComputerLapDeskTop, PrinterScanner, Screen, BioVayaNoteCounterGenerator,
                                      Atm, SwitchRouterFirewall, PhysicalNode, SystemHostedApplication)


class Branch(models.Model):
    code = models.PositiveIntegerField("Branch code", db_column="code", validators=[MinValueValidator(4000)], primary_key=True)
    name = models.CharField("Branch name", db_column="name", max_length=50, null=False, blank=False, unique=True)

    class Meta:
        db_table = "branches"
    
    def __str__(self):
        return f"{self.name}"
        

class EquityStore(models.Model):
    name = models.CharField("Name", max_length=50, db_column="name", unique=True, null=False, blank=False)

    class Meta:
        db_table = "equity_stores"
    
    def __str__(self):
        return f"{self.name} store"


class AssetAssignment(models.Model):
    assignment_num = models.BigAutoField("Assignment number", primary_key=True, db_column='assignment_num')
    approver = models.ForeignKey(User, verbose_name="Approver", related_name="approved_assignments", db_column="approver_id", on_delete=models.CASCADE)
    branch = models.CharField(verbose_name="Branch", db_column="branch", max_length=50, blank=False, null=False)
    exact_location = models.CharField(verbose_name="Exact location", db_column="exact_location", max_length=50, blank=False, null=False)
    approval_status = models.CharField(verbose_name="Approval status", max_length=20, db_column="approval_status", blank=False, null=False, default="Pending")
    status = models.CharField(verbose_name="Status", max_length=20, db_column="status", blank=False, null=False, default="Inactive")
    date_assigned = models.DateTimeField(verbose_name="Date assigned", default=datetime.now(), db_column="date_assigned")
    date_approved = models.DateTimeField(verbose_name="Date approved/rejected", db_column="date_approved", null=True)
    returned = models.BooleanField(verbose_name="Returned", db_column="returned", default=False)
    returned_date = models.DateTimeField(verbose_name="Returned date", db_column="returned_date", blank=True, null=True)
    return_reason = models.CharField(verbose_name="Return reason", max_length=200, db_column="return_reason", blank=False, null=False)
    external_movement_required = models.BooleanField(verbose_name="Required movement from head office", db_column="external_movement_required", blank=False, null=False)

    assigner = models.ForeignKey(User, verbose_name=("Assigner"), related_name="assigner_assignments", on_delete=models.CASCADE, db_column="assigner_id", null=True, blank=True)
    assignee = models.ForeignKey(User, verbose_name=("Assignee"), related_name="assignee_assignments", on_delete=models.CASCADE, db_column="assignee_id", null=True, blank=True)
    computer = models.ForeignKey(ComputerLapDeskTop, verbose_name="Computer", related_name="computer_assignments", on_delete=models.CASCADE, db_column="computer_id", null=True, blank=True)
    printer_scanner = models.ForeignKey(PrinterScanner, verbose_name="Printer/Scanner", related_name="printer_scanner_assignments", on_delete=models.CASCADE, db_column="printer_scanner_id", null=True, blank=True)
    screen = models.ForeignKey(Screen, verbose_name="Screen", related_name="screen_assignments", on_delete=models.CASCADE, db_column="screen_id", null=True, blank=True)
    bio_avaya_note_gen = models.ForeignKey(BioVayaNoteCounterGenerator, verbose_name="Bio/Avaya/note counter/generator", related_name="bio_avaya_note_gen_assignments", on_delete=models.CASCADE, db_column="bio_avaya_note_gen_id", null=True, blank=True)
    atm = models.ForeignKey(Atm, verbose_name="ATM", related_name="atm_assignments", on_delete=models.CASCADE, db_column="atm_id", null=True, blank=True)
    switch_router_firewall = models.ForeignKey(SwitchRouterFirewall, verbose_name="Switch Router Firewall", related_name="switch_router_frewall_assignments", on_delete=models.CASCADE, db_column="switch_router_firewall_id", null=True, blank=True)
    node = models.ForeignKey(PhysicalNode, verbose_name="Physical node", related_name="node_assignments", on_delete=models.CASCADE, db_column="node_id", null=True, blank=True)
    application = models.ForeignKey(SystemHostedApplication, verbose_name="Hosted application", related_name="application_assignments", on_delete=models.CASCADE, db_column="application_id", null=True, blank=True)


    class Meta:
        db_table = "asset_assignments"
        verbose_name = _('asset_assignment')
        verbose_name_plural = _('asset_assignments')
    

    def __str__(self):
        return f"Assigned to Location: {self.branch } - {self.exact_location}"


       

