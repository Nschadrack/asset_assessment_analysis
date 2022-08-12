import re
from django.shortcuts import render, redirect
from assets_management.models import ComputerLapDeskTop, PrinterScanner, Atm, BioVayaNoteCounterGenerator
from .models import MaintenanceLog
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin



class MaintenanceLogList(LoginRequiredMixin, View):

    def get(self, request, asset_id, category, *args, **kwargs):
        part_numbers = []
        if category == "ATM_MAINTENANCE":
            asset = Atm.objects.filter(pk=asset_id).first()
            part_numbers = [
                {
                    "serial_number": "123456",
                    "sparepart_name": "EEPROM"
                },
                {
                    "serial_number": "123457",
                    "sparepart_name": "BELT DOUBLE EXTRACTOR CMD V4"
                },
                {
                    "serial_number": "123458",
                    "sparepart_name": "CARD READER CHD V2CU STANDARD + ANTIM3"
                },
            ]
        context = {
            "asset": asset,
            "category": category,
            "part_numbers": part_numbers,
        }
        
        return render(request, "maintenance/maintenance_form.html", context)

    def post(self, request, asset_id, category, *args, **kwargs):
        maintenance_type = request.POST["maintenance_type"]
        maintenance_asset_category = request.POST["maintenance_asset_category"]
        ticket_type = re.sub("[\[\]']", "",str(request.POST.getlist("ticket_type")))
        environment_check = re.sub("[\[\]']", "", str(request.POST.getlist("environment_check")))
        areas_serviced = re.sub("[\[\]']", "", str(request.POST.getlist("areas_serviced")))
        additional_note = request.POST["additional_note"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        maintenance_cost = 150000
        spareparts_quantity_used = 5
        spareparts = request.POST.getlist("spareparts")

        maintenance_log = MaintenanceLog(
            maintenance_type=maintenance_type,
            maintenance_asset_category=maintenance_asset_category,
            ticket_type=ticket_type,
            environment_check=environment_check,
            areas_serviced=areas_serviced,
            additional_note=additional_note,
            start_date=start_date,
            end_date=end_date,
            maintenance_cost=maintenance_cost,
            spareparts_quantity_used=spareparts_quantity_used
        )
        print(f"""
        Actual data:\n
            maintenance_type: {maintenance_type}\n
            maintenance_asset_category: {maintenance_asset_category}\n
            ticket_type: {ticket_type}\n
            environment_check: {environment_check}\n
            areas_serviced: {areas_serviced}\n
            additional_note: {additional_note}\n
            start_date: {start_date}\n
            end_date: {end_date}\n
            maintenance_cost: {maintenance_cost}\n
            spareparts_quantity_used: {spareparts_quantity_used}\n
            spareparts: {spareparts}
        """)
        if category == "ATM_MAINTENANCE":
            asset = Atm.objects.filter(pk=asset_id).first()
        context = {
            "asset": asset,
            "category": category
        }
        print(f"Maintenance log post: {dict(request.POST)}")
        return redirect("assets_management:atms-list")
