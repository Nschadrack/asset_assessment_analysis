import re
from django.shortcuts import render, redirect
from assets_management.models import ComputerLapDeskTop, PrinterScanner, Atm, BioVayaNoteCounterGenerator
from .models import MaintenanceLog, SparePart
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin



class MaintenanceLogList(LoginRequiredMixin, View):

    def get(self, request, asset_id, category, *args, **kwargs):
        availabel_spareparts = []
        if category == "ATM_MAINTENANCE":
            asset = Atm.objects.filter(pk=asset_id).first()
            availabel_spareparts = SparePart.objects.filter(was_used=False, sparepart_category="ATM_SPAREPART")
        elif category == "COMPUTER_MAINTENANCE":
            asset = ComputerLapDeskTop.objects.filter(pk=asset_id).first()
            availabel_spareparts = SparePart.objects.filter(was_used=False, sparepart_category="COMPUTER_SPAREPART")
        elif category == "PRINTER_MAINTENANCE" or category == "SCANNER_MAINTENANCE":
            asset = PrinterScanner.objects.filter(pk=asset_id).first()
            availabel_spareparts = SparePart.objects.filter(was_used=False, sparepart_category="PRINTER_SCANNER_SPAREPART")
        elif category == "NOTE_COUNTER_MAINTENANCE":
            asset = PrinterScanner.objects.filter(pk=asset_id).first()
            availabel_spareparts = SparePart.objects.filter(was_used=False, sparepart_category="NOTE_COUNTER_SPAREPART")

        context = {
            "asset": asset,
            "category": category,
            "part_numbers": availabel_spareparts,
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
        spareparts = request.POST.getlist("spareparts")
        spareparts_quantity_used = len(spareparts)

        maintenance_cost = 0
        spareparts_save = []
        for spare_part in spareparts:
            serial_num = spare_part.split("|")[0].strip()
            sparepart = SparePart.objects.filter(serial_number=serial_num).first()
            maintenance_cost += sparepart.unit_price
            spareparts_save.append(sparepart)

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
        
        if category == "ATM_MAINTENANCE":
            asset = Atm.objects.filter(pk=asset_id).first()
            maintenance_log.atm = asset
        elif category == "COMPUTER_MAINTENANCE":
            asset = ComputerLapDeskTop.objects.filter(pk=asset_id).first()
            maintenance_log.computer = asset
        elif category == "PRINTER_MAINTENANCE" or category == "SCANNER_MAINTENANCE":
            asset = PrinterScanner.objects.filter(pk=asset_id).first()
            maintenance_log.printer_scanner = asset
        elif category == "NOTE_COUNTER_MAINTENANCE":
            asset = PrinterScanner.objects.filter(pk=asset_id).first()
            maintenance_log.note_counter = asset

        maintenance_log.save()
        for spare in spareparts_save:
            spare.maintenance_log = maintenance_log
            spare.was_used = True
            spare.save()
        

        if category == "ATM_MAINTENANCE":
            return HttpResponseRedirect(reverse("assets_management:atm-detail", args=(asset_id,)))

        elif category == "COMPUTER_MAINTENANCE":
            return HttpResponseRedirect(reverse("assets_management:computer-detail", args=(asset_id,)))

        elif category == "PRINTER_MAINTENANCE":
            return HttpResponseRedirect(reverse("assets_management:printer-detail", args=(asset_id,)))

        elif category == "SCANNER_MAINTENANCE":
            return HttpResponseRedirect(reverse("assets_management:scanner-detail", args=(asset_id,)))

        elif category == "NOTE_COUNTER_MAINTENANCE":
            return HttpResponseRedirect(reverse("assets_management:note-counter-detail", args=(asset_id,)))

        return redirect("assets_management:atms-list")


class SparepartList(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        spareparts = SparePart.objects.all()

        context = {
            "spareparts":spareparts,
            "SPAREPARTS_CATEGORIES": SparePart.SPAREPARTS_CATEGORIES
        }
        
        return render(request, "maintenance/spareparts-list.html", context)

    def post(self, request, *args, **kwargs):
        sparepart_category = request.POST["sparepart_category"] 
        serial_number = request.POST["serial_number"]
        sparepart_name = request.POST["sparepart_name"]
        unit_price = request.POST["unit_price"]
        delivery_date = request.POST["delivery_date"] 

        sparepart = SparePart(
            sparepart_category=sparepart_category,
            serial_number=serial_number,
            sparepart_name=sparepart_name,
            unit_price=unit_price,
            delivery_date=delivery_date
        )

        sparepart.save()

        return redirect("maintenance:spareparts-list")


class MaintenanceLogDetail(LoginRequiredMixin, View):
    def get(self, request, maintenance_id, *args, **kwargs):
        maintenance_log = MaintenanceLog.objects.filter(pk=maintenance_id).first() 
        spareparts = SparePart.objects.filter(maintenance_log=maintenance_log)

        context = {
            "maintenance_log":maintenance_log,
            "spareparts": spareparts,
            "maintenance_logs_spareparts_num": len(spareparts)
        }

        return render(request, "maintenance/maintenance-details.html", context)


