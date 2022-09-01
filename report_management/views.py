import pdfkit
from django.shortcuts import render
from django.http import FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from assets_management.models import (ComputerLapDeskTop, PrinterScanner, Screen, BioVayaNoteCounterGenerator,
                     Atm, SwitchRouterFirewall, PhysicalNode, SystemHostedApplication)




from json import dumps
import os 
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from assets_management.models import *
from maintenance.models import SparePart, MaintenanceLog
from assets_movement.models import Branch, AssetAssignment

def dashboard_report(request):
    laptops = ComputerLapDeskTop.objects.filter(still_functions=True, category="LAPTOP").count()
    desktops = ComputerLapDeskTop.objects.filter(still_functions=True, category="DESKTOP").count()
    printers = PrinterScanner.objects.filter(still_functions=True, category="PRINTER").count()
    scanners = PrinterScanner.objects.filter(still_functions=True, category="SCANNER").count()
    atms = Atm.objects.filter(still_functions=True).count()
    note_counters = BioVayaNoteCounterGenerator.objects.filter(still_functions=True, category="NOTE-COUNTER").count()
    bios = BioVayaNoteCounterGenerator.objects.filter(still_functions=True, category="BIO").count()
    avaya = BioVayaNoteCounterGenerator.objects.filter(still_functions=True, category="AVAYA").count()
    generators = BioVayaNoteCounterGenerator.objects.filter(still_functions=True, category="GENERATOR").count()
    servers = PhysicalNode.objects.filter(still_functions=True).count()
    tvs = Screen.objects.filter(still_functions=True, category="TV").count()
    monitors = Screen.objects.filter(still_functions=True, category="MONITOR").count()
    switches = SwitchRouterFirewall.objects.filter(still_functions=True, category="SWITCH").count()
    routers = SwitchRouterFirewall.objects.filter(still_functions=True, category="ROUTER").count()
    firewalls = SwitchRouterFirewall.objects.filter(still_functions=True, category="FIREWALL").count()
    applications = SystemHostedApplication.objects.filter(still_functions=True).count()

    all_assignments = AssetAssignment.objects.all()

    # computer status
    computers_status_list = ComputerLapDeskTop.objects.all()
    printers_scanners_status_list = PrinterScanner.objects.all()
    atms_status_list = Atm.objects.all()
    note_counters_status_list = BioVayaNoteCounterGenerator.objects.filter(category="NOTE-COUNTER")


    # Maintenance log for assets
    maintenance_logs = MaintenanceLog.objects.all()
    atm_maintenance_logs = [ log for log in maintenance_logs if log.atm is not None ]



    computer_assignments = [ assign for assign in all_assignments if assign.computer is not None]
    printer_scanner_assignments = [ assign for assign in all_assignments if assign.printer_scanner is not None]
    atms_assignments = [ assign for assign in all_assignments if assign.atm is not None]
    note_counters_assignments = [ assign for assign in all_assignments if assign.bio_avaya_note_gen is not None]

    laptops_assing = [assign for assign in computer_assignments if assign.computer.category=="LAPTOP" ]
    desktops_assing = [assign for assign in computer_assignments if assign.computer.category=="DESKTOP" ]
    printer_assing = [assign for assign in printer_scanner_assignments if assign.printer_scanner.category=="PRINTER" ]
    scanner_assing = [assign for assign in printer_scanner_assignments if assign.printer_scanner.category=="SCANNER" ]
    note_counters_assing = [assign for assign in note_counters_assignments if assign.bio_avaya_note_gen.category=="NOTE-COUNTER" ]

    branches_ = Branch.objects.all()
    branches = [branch.name for branch in branches_]
    branches = sorted(branches)

    desktops_dist = {}
    laptops_dist = {}
    atm_dist = {}
    printer_dist = {}
    scanner_dist = {}
    note_counter_dist = {}
    computers_status_dist = {}
    atm_status_dist = {}
    printers_scanners_status_dist = {}
    note_counters_status_dist = {}
    atm_maintenance_cost_dist = {}

    for maintenance_log in atm_maintenance_logs:
        atm_maintenance_cost_dist[maintenance_log.atm.hostname] = atm_maintenance_cost_dist.get(maintenance_log.atm.hostname, 0) + maintenance_log.maintenance_cost

    for status in CommonAsset.STATUES:
        computers_status_dist[status[0]] = 0
        atm_status_dist[status[0]] = 0
        printers_scanners_status_dist[status[0]] = 0
        note_counters_status_dist[status[0]] = 0

    for computer_status in computers_status_list:
        computers_status_dist[computer_status.status] = computers_status_dist.get(computer_status.status, 0) + 1
    
    for atm_status in atms_status_list:
        atm_status_dist[atm_status.status] = atm_status_dist.get(atm_status.status, 0) + 1
    
    for printer_scanner_status in printers_scanners_status_list:
        printers_scanners_status_dist[printer_scanner_status.status] = printers_scanners_status_dist.get(printer_scanner_status.status, 0) + 1
    
    for note_counter_status in note_counters_status_list:
        note_counters_status_dist[note_counter_status.status] = note_counters_status_dist.get(note_counter_status.status, 0) + 1

    for branch in branches:
        laptops_dist[branch] = laptops_dist.get(branch, 0)
        desktops_dist[branch] = desktops_dist.get(branch, 0)
        atm_dist[branch] = atm_dist.get(branch, 0)
        printer_dist[branch] = printer_dist.get(branch, 0)
        scanner_dist[branch] = scanner_dist.get(branch, 0)
        note_counter_dist[branch] = note_counter_dist.get(branch, 0)

    for lap_assign in laptops_assing:
        laptops_dist[lap_assign.branch] = laptops_dist.get(lap_assign.branch, 0) + 1
    laptops_dist = dict(sorted(laptops_dist.items(), key=lambda v:v[0]))
    for desk_assign in desktops_assing:
        desktops_dist[desk_assign.branch] = desktops_dist.get(desk_assign.branch, 0) + 1
    desktops_dist = dict(sorted(desktops_dist.items(), key=lambda v:v[0]))
    for atm_assign in atms_assignments:
        atm_dist[atm_assign.branch] = atm_dist.get(atm_assign.branch, 0) + 1
    atm_dist = dict(sorted(atm_dist.items(), key=lambda v:v[0]))
    for printer_assign in printer_assing:
        printer_dist[printer_assign.branch] = printer_dist.get(printer_assign.branch, 0) + 1
    printer_dist = dict(sorted(printer_dist.items(), key=lambda v:v[0]))
    for scanner_assign in scanner_assing:
        scanner_dist[scanner_assign.branch] = scanner_dist.get(scanner_assign.branch, 0) + 1
    scanner_dist = dict(sorted(scanner_dist.items(), key=lambda v:v[0]))
    for note_counter_assign in note_counters_assing:
        note_counter_dist[note_counter_assign.branch] = note_counter_dist.get(note_counter_assign.branch, 0) + 1
    note_counter_dist = dict(sorted(note_counter_dist.items(), key=lambda v:v[0]))

    colors = ["rgb(197, 124, 60)", "rgb(171, 98, 192)","rgb(114, 165, 85)","rgb(202, 86, 112)","rgb(99, 140, 204)"]
    colors.extend(["rgb(197, 124, 60)", "rgb(171, 98, 192)","rgb(114, 165, 85)","rgb(202, 86, 112)","rgb(99, 140, 204)"])
    colors.extend(["rgb(197, 124, 60)", "rgb(171, 98, 192)","rgb(114, 165, 85)","rgb(202, 86, 112)","rgb(99, 140, 204)"])
    colors.extend(["rgb(197, 124, 60)", "rgb(171, 98, 192)"])
    summary_statistics = [
        {
            "title": "Computers",
            "categories":{
                "Laptops": laptops,
                "Desktops": desktops
            },
            "total": (laptops + desktops)
        },
        {
            "title": "ATMS and Note Counters",
            "categories": {
                "atms": atms,
                "note_counters": note_counters
            },
            "total": (atms + note_counters)
        },
        {
            "title": "Scanners and Printers",
            "categories":{
                "Scanners": scanners,
                "Printers": printers
            },
            "total": (scanners + printers)
        },
        {
            "title": "AVAYA and Biometrics",
            "categories": {
                "AVAYA": avaya,
                "BIO": bios
            },
            "total": (avaya + bios)
        },
        {
            "title": "TVs and Monitors",
            "categories": {
                "TV": tvs,
                "monitors": monitors
            },
            "total": (tvs + monitors)
        },
        {
            "title": "Servers and Generators",
            "categories": {
                "Servers": servers,
                "generators": generators
            },
            "total": (servers + generators)
        },
        {
            "title": "Switches and Routers",
            "categories": {
                "Switches": switches,
                "routers": routers
            },
            "total": (switches + routers)
        },
        {
            "title": "Applications and Firewalls",
            "categories": {
                "applications": applications,
                "firewalls": firewalls
            },
            "total": (applications + firewalls)
        }
    ]

    computer_data_dist = {
				"labels": branches,
				"datasets": [
					{
						"label": "Desktops",
						"data": list(desktops_dist.values()),
						"backgroundColor": colors[0]
					},
					{
						"label": "Laptops",
						"data":list(laptops_dist.values()),
						"backgroundColor": colors[3]
					}
				]
	        }
    printer_scanner_data_dist = {
				"labels": branches,
				"datasets": [
					{
						"label": "Printers",
						"data": list(printer_dist.values()),
						"backgroundColor": colors[0]
					},
					{
						"label": "Scanners",
						"data":list(scanner_dist.values()),
						"backgroundColor": colors[3]
					}
				]
	        }
    atm_data_dist = {
				"labels": branches,
				"datasets": [
					{
						"label": "ATM",
						"data": list(atm_dist.values()),
						"backgroundColor": colors
					},
				]
	        }
    note_counter_data_dist = {
				"labels": branches,
				"datasets": [
					{
						"label": "Note Counters",
						"data": list(note_counter_dist.values()),
						"backgroundColor": colors
					},
				]
	        }
    computers_status_dist_data = {
				"labels": list(computers_status_dist.keys()),
				"datasets": [
					{
						"label": "Working status for computers",
						"data": list(computers_status_dist.values()),
						"backgroundColor": ["rgb(171, 98, 192)","rgb(114, 165, 85)","rgb(202, 86, 112)","rgb(99, 140, 204)"]
					},
				]
	        }
    printers_scanners_status_data = {
				"labels": list(printers_scanners_status_dist.keys()),
				"datasets": [
					{
						"label": "Working status for computers",
						"data": list(printers_scanners_status_dist.values()),
						"backgroundColor": ["rgb(171, 98, 192)","rgb(114, 165, 85)","rgb(202, 86, 112)","rgb(99, 140, 204)"]
					},
				]
	        }
    note_counters_status_dist_data = {
				"labels": list(note_counters_status_dist.keys()),
				"datasets": [
					{
						"label": "Working status for note counters",
						"data": list(note_counters_status_dist.values()),
						"backgroundColor": ["rgb(171, 98, 192)","rgb(114, 165, 85)","rgb(202, 86, 112)","rgb(99, 140, 204)"]
					},
				]
	        }
    atm_status_dist_data = {
				"labels": list(atm_status_dist.keys()),
				"datasets": [
					{
						"label": "Working status for ATM",
						"data": list(atm_status_dist.values()),
						"backgroundColor": ["rgb(171, 98, 192)","rgb(114, 165, 85)","rgb(202, 86, 112)","rgb(99, 140, 204)"]
					},
				]
	        }
    atm_maintenance_cost_dist_data = {
				"labels": list(atm_maintenance_cost_dist.keys()),
				"datasets": [
					{
						"label": "Working status for ATM",
						"data": [float(value) for value in list(atm_maintenance_cost_dist.values())],
						"backgroundColor": "rgb(171, 98, 192)",
					},
				]
	        }

    context = {
        "summary_statistics": summary_statistics,
        "computersDistributionData": dumps(computer_data_dist),
        "printerScannerDistributionData": dumps(printer_scanner_data_dist),
        "atmDistributionData": dumps(atm_data_dist),
        "noteCounterDistributionData": dumps(note_counter_data_dist),
        "computersStatusDistData": dumps(computers_status_dist_data),
        "atmStatusDistData": dumps(atm_status_dist_data),
        "printerScannerStatusDistData": dumps(printers_scanners_status_data),
        "noteCounterStatusDistData": dumps(note_counters_status_dist_data),
        "atmMaintenanceCostDistData": dumps(atm_maintenance_cost_dist_data)
        
    }

    return render(request, 'report_management/dashboard.html', context)


class ComputersListReport(View):
    def get(self, request, *args,**kwargs):
        computers = ComputerLapDeskTop.objects.all().order_by('-recorded_date')
        context = {
            "computers": computers,
            "COMPUTER_CATEGORIES": ComputerLapDeskTop.CATEGORIES,
            "STORAGE_TYPES": ComputerLapDeskTop.STORAGE_TYPES,
            "MEASUREMENTS": ComputerLapDeskTop.MEASUREMENTS,
            "PROCESSOR_MANUFACTURES": ComputerLapDeskTop.PROCESSOR_MANUFACTURES,
            "PROCESSOR_TYPES": ComputerLapDeskTop.PROCESSOR_TYPES,
            "PROCESSOR_SPEED_MEASUREMENTS": ComputerLapDeskTop.PROCESSOR_SPEED_MEASUREMENTS,
            "STORES": ComputerLapDeskTop.STORES,
            "STATUES": ComputerLapDeskTop.STATUES 
        }
        return render(request, 'report_management/computers.html', context)
    

class PrintersListReport(View):
    def get(self, request, report=None, *args, **kwargs):
        printers = PrinterScanner.objects.filter(category='PRINTER').order_by('-recorded_date')
        context = {
            "printers": printers,
            "CATEGORY_TYPES": PrinterScanner.PRINTER_CATEGORY_TYPES,
            "CONNECTION_TYPES": PrinterScanner.CONNECTION_TYPES,
            "STORES": PrinterScanner.STORES,
            "STATUES": PrinterScanner.STATUES
        }
        return render(request, 'report_management/printers.html', context)


class ScannersListReport(View):
    def get(self, request, report=None, *args, **kwargs):
        scanners = PrinterScanner.objects.filter(category='SCANNER').order_by('-recorded_date')
        context = {
            "scanners": scanners,
            "CATEGORY_TYPES": PrinterScanner.SCANNER_CATEGORY_TYPES,
            "CONNECTION_TYPES": PrinterScanner.CONNECTION_TYPES,
            "STORES": PrinterScanner.STORES,
            "STATUES": PrinterScanner.STATUES
        }

        return render(request, 'report_management/scanners.html', context)


class NoteCountersListReport(View):
    def get(self, request, report=None, *args, **kwargs):
        note_counters = BioVayaNoteCounterGenerator.objects.filter(category="NOTE-COUNTER").order_by('-recorded_date')
        context = {
            "note_counters": note_counters,
            "STORES": BioVayaNoteCounterGenerator.STORES,
            "STATUES": BioVayaNoteCounterGenerator.STATUES,
        }

        return render(request, 'report_management/note-counters.html', context)


class AtmsListReport(View):
    def get(self, request, report=None, *args, **kwargs):
        atms = Atm.objects.all().order_by('-recorded_date')
        context = {
            "atms": atms,
            "STORES": Atm.STORES,
            "STATUES": Atm.STATUES,
        }

        return render(request, 'report_management/atms.html', context)




