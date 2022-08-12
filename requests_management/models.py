from django.db import models
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from assets_movement.models import AssetAssignment 
from users_management.models import User




class RequestAssignment(models.Model):
    # REQUEST_TYPES = (
    #     ("COMPUTER ASSIGNMENT", "COMPUTER ASSIGNMENT"),
    #     ("PRINTER ASSIGNMENT", "PRINTER ASSIGNMENT"),
    #     ("SCANNER ASSIGNMENT", "SCANNER ASSIGNMENT"),
    #     ("SCREEN ASSIGNMENT", "SCREEN ASSIGNMENT"),
    #     ("BIOMETRIC DEVICE ASSIGNMENT", "BIOMETRIC DEVICE ASSIGNMENT"),
    #     ("AVAYA ASSIGNMENT", "AVAYA ASSIGNMENT"),
    #     ("NOTE COUNTER ASSIGNMENT", "NOTE COUNTER ASSIGNMENT"),
    #     ("ATM ASSIGNMENT", "ATM ASSIGNMENT"),
    #     ("GENERATOR ASSIGNMENT", "GENERATOR ASSIGNMENT"),
    #     ("SWITCH ASSIGNMENT", "SWITCH ASSIGNMENT"),
    #     ("ROUTER ASSIGNMENT", "ROUTER ASSIGNMENT"),
    #     ("FIREWALL ASSIGNMENT", "FIREWALL ASSIGNMENT"),
    #     ("PHYSICAL SERVER ASSIGNMENT", "PHYSICAL SERVER ASSIGNMENT"),
    #     ("OTHER ASSETS CATEGORY ASSIGNMENT", "OTHER ASSETS CATEGORY ASSIGNMENT"),
    #     ("HOSTED APPLICATION ASSIGNMENT", "HOSTED APPLICATION ASSIGNMENT"),
    # )

    request_id = models.BigAutoField(verbose_name="Request id", db_column="request_id", primary_key=True)
    request_type = models.CharField(verbose_name="Request type", db_column="request_type", max_length=40, blank=False, null=False)
    status = models.CharField(verbose_name="Status", db_column="status", blank=False, null=False, default="Pending", max_length=15)
    rejection_note = models.TextField(verbose_name="Rejection note", db_column="rejection_note", null=True, blank=True)
    assignment_id = models.ForeignKey(AssetAssignment, verbose_name="Asset assignment", related_name="assignment_requests", db_column="assignment_id", on_delete=models.CASCADE)
    approver = models.ForeignKey(User, verbose_name="Approver", related_name="requests_to_me", db_column="approver_id", on_delete=models.CASCADE)
    assigner = models.ForeignKey(User, verbose_name="Assigner", related_name="my_requests", db_column="assigner_id", on_delete=models.CASCADE)
    opened_date = models.DateTimeField(verbose_name="Opened date", default=datetime.now(), db_column='opened_date')

    class Meta:
        db_table = "request_assignments"
        verbose_name = _('request_assignment')
        verbose_name_plural = _('request_assignments')
