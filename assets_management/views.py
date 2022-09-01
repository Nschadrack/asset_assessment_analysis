import pdfkit
import os
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import View
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import (ComputerLapDeskTop, PrinterScanner, Screen, BioVayaNoteCounterGenerator,
                     Atm, SwitchRouterFirewall, PhysicalNode, SystemHostedApplication)
from .serializers import (ComputerLapDeskTopSerializer, PrinterScannerSerializer, ScreenSerializer, BioVayaNoteCounterGeneratorSerializer, AtmSerializer,
                          SwitchRouterFirewallSerializer, PhysicalNodeSerializer, SystemHostedApplicationSerializer)

from assets_movement.models import AssetAssignment
from maintenance.models import MaintenanceLog

from .utils import *

options = {
    'page-size': 'A1',
    'margin-top': '0.55in',
    'margin-right': '0.05in',
    'margin-bottom': '0.55in',
    'margin-left': '0.05in',
}

class ComputersList(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"

    def get(self, request, report=None, *args,**kwargs):
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
        
        if report == 'report':
            filename = os.path.join("dashboard\\static\\reports\\computers.pdf")
            pdfkit.from_url("http://localhost:8000/report/computers/", filename, verbose=True, options=options)
            return FileResponse(open(filename, "rb"), content_type="application/pdf")
        return render(request, 'assets_management/computers-list.html', context)

    def post(self, request, *args, **kwargs):
        serializer = ComputerLapDeskTopSerializer(data=request.POST, context={'request': request})
        if serializer.is_valid():
            valid_tag_number = not is_asset_exist_with_tag_number(serializer.validated_data["tag_number"])
            if valid_tag_number:
                serializer.save()
            else:
                #some error messages
                if not valid_tag_number:
                    print(
                        f"\n\nTag number {serializer.data['tag_number']} already exists\n\n")
        else:
            print(f"\n\nErrors: {serializer.errors}")
        return redirect("assets_management:computers-list")


class ComputerDetail(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get_object(self, pk):
        try:
            return ComputerLapDeskTop.objects.get(asset_id=pk) 
        except:
            return None 
    
    def get(self, request, pk, update_or_delete=None, *args, **kwargs):
        computer = self.get_object(pk)
        if computer:
            computer_users = AssetAssignment.objects.filter(computer=computer, approval_status="Approved")
            maintenance_logs = MaintenanceLog.objects.filter(computer=computer)
            context = {
                "computer": computer,
                "maintenance_logs": maintenance_logs,
                "maintenance_logs_num": len(maintenance_logs),
                "computer_users":computer_users,
                "assignments_num": len(computer_users),
                "COMPUTER_CATEGORIES": ComputerLapDeskTop.CATEGORIES,
                "STORAGE_TYPES": ComputerLapDeskTop.STORAGE_TYPES,
                "MEASUREMENTS": ComputerLapDeskTop.MEASUREMENTS,
                "PROCESSOR_MANUFACTURES": ComputerLapDeskTop.PROCESSOR_MANUFACTURES,
                "PROCESSOR_TYPES": ComputerLapDeskTop.PROCESSOR_TYPES,
                "PROCESSOR_SPEED_MEASUREMENTS": ComputerLapDeskTop.PROCESSOR_SPEED_MEASUREMENTS,
                "STORES": ComputerLapDeskTop.STORES,
                "STATUES": ComputerLapDeskTop.STATUES 
            }
            
            if update_or_delete=="update":
                return render(request, 'assets_management/computer-update-form.html', context)
            if update_or_delete == "confirm_delete":
                context = {
                "category": "computer", 
                "asset": computer,
                "cancel_url_name": "assets_management:computer-detail",
                "list_url": "assets_management:printers-list",
                "asset_id": computer.asset_id,
                "delete_url_name": "assets_management:computer-detail-update"
                }
                return render(request, 'assets_management/asking_delete_confirm.html', context)
            if update_or_delete == "delete":
                if self.delete(request, pk):
                    return redirect("assets_management:computers-list")
            return render(request, 'assets_management/computer-details.html', context)
        return redirect("assets_management:computers-list")

    def post(self, request, pk, update_or_delete="update", format=None):
        computer = self.get_object(pk)
        if computer:
            serializer = ComputerLapDeskTopSerializer(data=request.POST, instance=computer, context={'request': request})
            if serializer.is_valid():
                    serializer.save()
            else:
                print(f"\n\nErrors: {serializer.errors}")
        return HttpResponseRedirect(reverse("assets_management:computer-detail", args=(pk,)))

    
    def delete(self, request, pk, format=None):
        computer = self.get_object(pk)
        if computer:
            computer.delete()
            return True 
        return False


class PrintersList(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, report=None, *args, **kwargs):
        printers = PrinterScanner.objects.filter(category='PRINTER').order_by('-recorded_date')
        context = {
            "printers": printers,
            "CATEGORY_TYPES": PrinterScanner.PRINTER_CATEGORY_TYPES,
            "CONNECTION_TYPES": PrinterScanner.CONNECTION_TYPES,
            "STORES": PrinterScanner.STORES,
            "STATUES": PrinterScanner.STATUES
        }
        if report == 'report':
            filename = os.path.join("dashboard\\static\\reports\\printers.pdf")
            pdfkit.from_url("http://localhost:8000/report/printers/", filename, verbose=True, options=options)
            return FileResponse(open(filename, "rb"), content_type="application/pdf")
        return render(request, 'assets_management/printers-list.html', context)
    
    def post(self, request, *args, **kwargs):
        serializer = PrinterScannerSerializer(data=request.POST, context={'request': request})
        if serializer.is_valid():
            valid_tag_number = not is_asset_exist_with_tag_number(serializer.validated_data["tag_number"])
            valid_host_ip = not is_asset_exist_with_host_ip(serializer.validated_data["host_ip"])
            if valid_host_ip and valid_tag_number:
                serializer.save()
            else:
                #some error messages
                if not valid_tag_number:
                    print(
                        f"\n\nTag number {serializer.data['tag_number']} already exists\n\n")
                if not valid_host_ip:
                    print(
                        f"\n\nHost IP {serializer.data['host_ip']} already exists\n\n")
        else:
            print(f"\n\nErrors: {serializer.errors}")
        return redirect("assets_management:printers-list")


class PrinterDetail(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get_object(self, pk):
        try:
            return PrinterScanner.objects.get(asset_id=pk)
        except:
            return None

    def get(self, request, pk, update_or_delete=None, *args, **kwargs):
        printer = self.get_object(pk)
        printer_users = AssetAssignment.objects.filter(printer_scanner=printer, approval_status="Approved")
        maintenance_logs = MaintenanceLog.objects.filter(printer_scanner=printer)
        if printer:
            context = {
                "printer": printer,
                "maintenance_logs": maintenance_logs,
                "maintenance_logs_num": len(maintenance_logs),
                "printer_users": printer_users,
                "assignments_num": len(printer_users),
                "CATEGORY_TYPES": PrinterScanner.PRINTER_CATEGORY_TYPES,
                "CONNECTION_TYPES": PrinterScanner.CONNECTION_TYPES,
                "STORES": PrinterScanner.STORES,
                "STATUES": PrinterScanner.STATUES
            }
            if update_or_delete == "update":
                return render(request, 'assets_management/printer-update-form.html', context)
            if update_or_delete == "confirm_delete":
                context = {
                    "category": "printer",
                    "asset": printer,
                    "cancel_url_name": "assets_management:printer-detail",
                    "list_url": "assets_management:printers-list",
                    "asset_id": printer.asset_id,
                    "delete_url_name": "assets_management:printer-detail-update"
                }
                return render(request, 'assets_management/asking_delete_confirm.html', context)
            if update_or_delete == "delete":
                if self.delete(request, pk):
                    return redirect("assets_management:printers-list")
            return render(request, 'assets_management/printer-details.html', context)
        return redirect("assets_management:printers-list")

    def post(self, request, pk, update_or_delete="update", format=None):
        printer = self.get_object(pk)
        if printer:
            serializer = PrinterScannerSerializer(data=request.POST, instance=printer, context={'request': request})
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"\n\nErrors: {serializer.errors}")
        return HttpResponseRedirect(reverse("assets_management:printer-detail", args=(pk,)))

    def delete(self, request, pk, format=None):
        printer = self.get_object(pk)
        if printer:
            printer.delete()
            return True
        return False


class ScannersList(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, report=None, *args, **kwargs):
        scanners = PrinterScanner.objects.filter(category='SCANNER').order_by('-recorded_date')
        context = {
            "scanners": scanners,
            "CATEGORY_TYPES": PrinterScanner.SCANNER_CATEGORY_TYPES,
            "CONNECTION_TYPES": PrinterScanner.CONNECTION_TYPES,
            "STORES": PrinterScanner.STORES,
            "STATUES": PrinterScanner.STATUES
        }
        if report == 'report':
            filename = os.path.join("dashboard\\static\\reports\\scanners.pdf")
            pdfkit.from_url("http://localhost:8000/report/scanners/", filename, verbose=True, options=options)
            return FileResponse(open(filename, "rb"), content_type="application/pdf")
        return render(request, 'assets_management/scanners-list.html', context)
    
    def post(self, request, *args, **kwargs):
        serializer = PrinterScannerSerializer(data=request.POST, context={'request': request})
        if serializer.is_valid():
            valid_tag_number = not is_asset_exist_with_tag_number(serializer.validated_data["tag_number"])
            valid_host_ip = not is_asset_exist_with_host_ip(serializer.validated_data["host_ip"])
            if valid_host_ip and valid_tag_number:
                serializer.save()
            else:
                #some error messages
                if not valid_tag_number:
                    print(f"\n\nTag number {serializer.data['tag_number']} already exists\n\n")
                if not valid_host_ip:
                    print(f"\n\nHost IP {serializer.data['host_ip']} already exists\n\n")
        else:
            print(f"\n\nErrors: {serializer.errors}")
        return redirect("assets_management:scanners-list")


class ScannerDetail(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get_object(self, pk):
        try:
            return PrinterScanner.objects.get(asset_id=pk)
        except:
            return None

    def get(self, request, pk, update_or_delete=None, *args, **kwargs):
        scanner = self.get_object(pk)
        scanner_users = AssetAssignment.objects.filter(printer_scanner=scanner, approval_status="Approved")
        maintenance_logs = MaintenanceLog.objects.filter(printer_scanner=scanner)
        if scanner:
            context = {
                "scanner": scanner,
                "maintenance_logs": maintenance_logs,
                "maintenance_logs_num": len(maintenance_logs),
                "assignments_num": len(scanner_users),
                "scanner_users": scanner_users,
                "CATEGORY_TYPES": PrinterScanner.PRINTER_CATEGORY_TYPES,
                "CONNECTION_TYPES": PrinterScanner.CONNECTION_TYPES,
                "STORES": PrinterScanner.STORES,
                "STATUES": PrinterScanner.STATUES
            }
            if update_or_delete == "update":
                return render(request, 'assets_management/scanner-update-form.html', context)
            if update_or_delete == "confirm_delete":
                context = {
                    "category": "scanner",
                    "asset": scanner,
                    "cancel_url_name": "assets_management:scanner-detail",
                    "list_url": "assets_management:scanners-list",
                    "asset_id": scanner.asset_id,
                    "delete_url_name": "assets_management:scanner-detail-update"
                }
                return render(request, 'assets_management/asking_delete_confirm.html', context)
            if update_or_delete == "delete":
                if self.delete(request, pk):
                    return redirect("assets_management:scanners-list")
            return render(request, 'assets_management/scanner-details.html', context)
        return redirect("assets_management:scanners-list")

    def post(self, request, pk, update_or_delete="update", format=None):
        scanner = self.get_object(pk)
        if scanner:
            serializer = PrinterScannerSerializer(data=request.POST, instance=scanner, context={'request': request})
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"\n\nErrors: {serializer.errors}")
        return HttpResponseRedirect(reverse("assets_management:scanner-detail", args=(pk,)))

    def delete(self, request, pk, format=None):
        scanner = self.get_object(pk)
        if scanner:
            scanner.delete()
            return True
        return False


class ScreensList(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, *args, **kwargs):
        screens = Screen.objects.all().order_by('-recorded_date')
        context = {
            "screens": screens,
            "STORES": Screen.STORES,
            "STATUES": Screen.STATUES,
            "CATEGORIES": Screen.CATEGORIES
        }
        return render(request, 'assets_management/screens-list.html', context)

    def post(self, request, *args, **kwargs):
        serializer = ScreenSerializer(data=request.POST, context={'request': request})
        if serializer.is_valid():
            valid_tag_number = not is_asset_exist_with_tag_number(serializer.validated_data["tag_number"])
            if valid_tag_number:
                serializer.save()
            else:
                #some error messages
                if not valid_tag_number:
                    print(
                        f"\n\nTag number {serializer.data['tag_number']} already exists\n\n")
        else:
            print(f"\n\nErrors: {serializer.errors}")
        return redirect("assets_management:screens-list")


class ScreenDetail(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get_object(self, pk):
        try:
            return Screen.objects.get(asset_id=pk)
        except:
            return None

    def get(self, request, pk, update_or_delete=None, *args, **kwargs):
        screen = self.get_object(pk)
        screen_users = AssetAssignment.objects.filter(screen=screen, approval_status="Approved")
        if screen:
            context = {
                "screen": screen,
                "screen_users": screen_users,
                "assignments_num": len(screen_users),
                "STORES": Screen.STORES,
                "STATUES": Screen.STATUES,
                "CATEGORIES": Screen.CATEGORIES
            }
            if update_or_delete == "update":
                return render(request, 'assets_management/screen-update-form.html', context)
            if update_or_delete == "confirm_delete":
                context = {
                    "category": "screen",
                    "asset": screen,
                    "cancel_url_name": "assets_management:screen-detail",
                    "list_url": "assets_management:screens-list",
                    "asset_id": screen.asset_id,
                    "delete_url_name": "assets_management:screen-detail-update"
                }
                return render(request, 'assets_management/asking_delete_confirm.html', context)
            if update_or_delete == "delete":
                if self.delete(request, pk):
                    return redirect("assets_management:screens-list")
            return render(request, 'assets_management/screen-details.html', context)
        return redirect("assets_management:screens-list")

    def post(self, request, pk, update_or_delete="update", format=None):
        screen = self.get_object(pk)
        if screen:
            serializer = ScreenSerializer(data=request.POST, instance=screen, context={'request': request})
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"\n\nErrors: {serializer.errors}")
        return HttpResponseRedirect(reverse("assets_management:screen-detail", args=(pk,)))

    def delete(self, request, pk, format=None):
        screen = self.get_object(pk)
        if screen:
            screen.delete()
            return True
        return False


class BiometricsList(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, *args, **kwargs):
        bios = BioVayaNoteCounterGenerator.objects.filter(category="BIO").order_by('-recorded_date')
        context = {
            "bios": bios,
            "STORES": BioVayaNoteCounterGenerator.STORES,
            "STATUES": BioVayaNoteCounterGenerator.STATUES,
        }
        return render(request, 'assets_management/bios-list.html', context)

    def post(self, request, *args, **kwargs):
        serializer = BioVayaNoteCounterGeneratorSerializer(
            data=request.POST, context={'request': request})
        if serializer.is_valid():
            valid_tag_number = not is_asset_exist_with_tag_number(serializer.validated_data["tag_number"])
            if valid_tag_number:
                serializer.save()
            else:
                #some error messages
                if not valid_tag_number:
                    print(
                        f"\n\nTag number {serializer.data['tag_number']} already exists\n\n")
        else:
            print(f"\n\nErrors: {serializer.errors}")
        return redirect("assets_management:biometrics-list")


class BiometricDetail(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get_object(self, pk):
        try:
            return BioVayaNoteCounterGenerator.objects.get(asset_id=pk)
        except:
            return None

    def get(self, request, pk, update_or_delete=None, *args, **kwargs):
        bio = self.get_object(pk)
        bio_users = AssetAssignment.objects.filter(bio_avaya_note_gen=bio, approval_status="Approved")
        if bio:
            context = {
                "bio": bio,
                "bio_users": bio_users,
                "assignments_num": len(bio_users),
                "STORES": BioVayaNoteCounterGenerator.STORES,
                "STATUES": BioVayaNoteCounterGenerator.STATUES,
            }
            if update_or_delete == "update":
                return render(request, 'assets_management/bio-update-form.html', context)
            if update_or_delete == "confirm_delete":
                context = {
                    "category": "biometric device",
                    "asset": bio,
                    "cancel_url_name": "assets_management:biometric-detail",
                    "list_url": "assets_management:biometrics-list",
                    "asset_id": bio.asset_id,
                    "delete_url_name": "assets_management:biometric-detail-update"
                }
                return render(request, 'assets_management/asking_delete_confirm.html', context)
            if update_or_delete == "delete":
                if self.delete(request, pk):
                    return redirect("assets_management:biometrics-list")
            return render(request, 'assets_management/biometric-details.html', context)
        return redirect("assets_management:biometrics-list")

    def post(self, request, pk, update_or_delete="update", format=None):
        bio = self.get_object(pk)
        if bio:
            serializer = BioVayaNoteCounterGeneratorSerializer(data=request.POST, instance=bio, context={'request': request})
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"\n\nErrors: {serializer.errors}")
        return HttpResponseRedirect(reverse("assets_management:biometric-detail", args=(pk,)))

    def delete(self, request, pk, format=None):
        bio = self.get_object(pk)
        if bio:
            bio.delete()
            return True
        return False


class AvayaList(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, *args, **kwargs):
        avayas = BioVayaNoteCounterGenerator.objects.filter(category="AVAYA").order_by('-recorded_date')
        context = {
            "avayas": avayas,
            "STORES": BioVayaNoteCounterGenerator.STORES,
            "STATUES": BioVayaNoteCounterGenerator.STATUES,
        }
        return render(request, 'assets_management/avaya-list.html', context)

    def post(self, request, *args, **kwargs):
        serializer = BioVayaNoteCounterGeneratorSerializer(data=request.POST, context={'request': request})
        if serializer.is_valid():
            valid_tag_number = not is_asset_exist_with_tag_number(serializer.validated_data["tag_number"])
            if valid_tag_number:
                serializer.save()
            else:
                #some error messages
                if not valid_tag_number:
                    print(
                        f"\n\nTag number {serializer.data['tag_number']} already exists\n\n")
        else:
            print(f"\n\nErrors: {serializer.errors}")
        return redirect("assets_management:avaya-list")


class AvayaDetail(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get_object(self, pk):
        try:
            return BioVayaNoteCounterGenerator.objects.get(asset_id=pk)
        except:
            return None

    def get(self, request, pk, update_or_delete=None, *args, **kwargs):
        avaya = self.get_object(pk)
        avaya_users = AssetAssignment.objects.filter(bio_avaya_note_gen=avaya, approval_status="Approved")
        if avaya:
            context = {
                "avaya": avaya,
                "avaya_users": avaya_users,
                "assignments_num": len(avaya_users),
                "STORES": BioVayaNoteCounterGenerator.STORES,
                "STATUES": BioVayaNoteCounterGenerator.STATUES,
            }
            if update_or_delete == "update":
                return render(request, 'assets_management/avaya-update-form.html', context)
            if update_or_delete == "confirm_delete":
                context = {
                    "category": "avaya",
                    "asset": avaya,
                    "cancel_url_name": "assets_management:avaya-detail",
                    "list_url": "assets_management:avaya-list",
                    "asset_id": avaya.asset_id,
                    "delete_url_name": "assets_management:avaya-detail-update"
                }
                return render(request, 'assets_management/asking_delete_confirm.html', context)
            if update_or_delete == "delete":
                if self.delete(request, pk):
                    return redirect("assets_management:avaya-list")
            return render(request, 'assets_management/avaya-details.html', context)
        return redirect("assets_management:avaya-list")

    def post(self, request, pk, update_or_delete="update", format=None):
        avaya = self.get_object(pk)
        if avaya:
            serializer = BioVayaNoteCounterGeneratorSerializer(data=request.POST, instance=avaya, context={'request': request})
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"\n\nErrors: {serializer.errors}")
        return HttpResponseRedirect(reverse("assets_management:avaya-detail", args=(pk,)))

    def delete(self, request, pk, format=None):
        avaya = self.get_object(pk)
        if avaya:
            avaya.delete()
            return True
        return False


class NoteCountersList(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, report=None, *args, **kwargs):
        note_counters = BioVayaNoteCounterGenerator.objects.filter(category="NOTE-COUNTER").order_by('-recorded_date')
        context = {
            "note_counters": note_counters,
            "STORES": BioVayaNoteCounterGenerator.STORES,
            "STATUES": BioVayaNoteCounterGenerator.STATUES,
        }
        if report == 'report':
            filename = os.path.join("dashboard\\static\\reports\\noteCounters.pdf")
            pdfkit.from_url("http://localhost:8000/report/note-counters/", filename, verbose=True, options=options)
            return FileResponse(open(filename, "rb"), content_type="application/pdf")
        return render(request, 'assets_management/note-counters-list.html', context)

    def post(self, request, *args, **kwargs):
        serializer = BioVayaNoteCounterGeneratorSerializer(data=request.POST, context={'request': request})
        if serializer.is_valid():
            valid_tag_number = not is_asset_exist_with_tag_number(serializer.validated_data["tag_number"])
            if valid_tag_number:
                serializer.save()
            else:
                #some error messages
                if not valid_tag_number:
                    print(
                        f"\n\nTag number {serializer.data['tag_number']} already exists\n\n")
        else:
            print(f"\n\nErrors: {serializer.errors}")
        return redirect("assets_management:avaya-list")


class NoteCounterDetail(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get_object(self, pk):
        try:
            return BioVayaNoteCounterGenerator.objects.get(asset_id=pk)
        except:
            return None

    def get(self, request, pk, update_or_delete=None, *args, **kwargs):
        note_counter = self.get_object(pk)
        note_counter_users = AssetAssignment.objects.filter(bio_avaya_note_gen=note_counter, approval_status="Approved")
        maintenance_logs = MaintenanceLog.objects.filter(note_counter=note_counter)
        if note_counter:
            context = {
                "note_counter": note_counter,
                "maintenance_logs":maintenance_logs,
                "maintenance_logs_num": len(maintenance_logs),
                "note_counter_users": note_counter_users,
                "assignments_num": len(note_counter_users),
                "STORES": BioVayaNoteCounterGenerator.STORES,
                "STATUES": BioVayaNoteCounterGenerator.STATUES,
            }
            if update_or_delete == "update":
                return render(request, 'assets_management/note-counter-update-form.html', context)
            if update_or_delete == "confirm_delete":
                context = {
                    "category": "note_counter",
                    "asset": note_counter,
                    "cancel_url_name": "assets_management:note-counter-detail",
                    "list_url": "assets_management:note-counters-list",
                    "asset_id": note_counter.asset_id,
                    "delete_url_name": "assets_management:note-counter-detail-update"
                }
                return render(request, 'assets_management/asking_delete_confirm.html', context)
            if update_or_delete == "delete":
                if self.delete(request, pk):
                    return redirect("assets_management:note-counters-list")
            return render(request, 'assets_management/note-counter-details.html', context)
        return redirect("assets_management:note-counters-list")

    def post(self, request, pk, update_or_delete="update", format=None):
        note_counter = self.get_object(pk)
        if note_counter:
            serializer = BioVayaNoteCounterGeneratorSerializer(data=request.POST, instance=note_counter, context={'request': request})
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"\n\nErrors: {serializer.errors}")
        return HttpResponseRedirect(reverse("assets_management:note-counter-detail", args=(pk,)))

    def delete(self, request, pk, format=None):
        note_counter = self.get_object(pk)
        if note_counter:
            note_counter.delete()
            return True
        return False


class GeneratorsList(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, *args, **kwargs):
        generators = BioVayaNoteCounterGenerator.objects.filter(category="GENERATOR").order_by('-recorded_date')
        context = {
            "generators": generators,
            "STORES": BioVayaNoteCounterGenerator.STORES,
            "STATUES": BioVayaNoteCounterGenerator.STATUES,
        }
        return render(request, 'assets_management/generators-list.html', context)

    def post(self, request, *args, **kwargs):
        serializer = BioVayaNoteCounterGeneratorSerializer(data=request.POST, context={'request': request})
        if serializer.is_valid():
            valid_tag_number = not is_asset_exist_with_tag_number(
                serializer.validated_data["tag_number"])
            if valid_tag_number:
                serializer.save()
            else:
                #some error messages
                if not valid_tag_number:
                    print(
                        f"\n\nTag number {serializer.data['tag_number']} already exists\n\n")
        else:
            print(f"\n\nErrors: {serializer.errors}")
        return redirect("assets_management:generators-list")


class GeneratorDetail(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get_object(self, pk):
        try:
            return BioVayaNoteCounterGenerator.objects.get(asset_id=pk)
        except:
            return None

    def get(self, request, pk, update_or_delete=None, *args, **kwargs):
        generator = self.get_object(pk)
        generator_users = AssetAssignment.objects.filter(bio_avaya_note_gen=generator, approval_status="Approved")
        if generator:
            context = {
                "generator": generator,
                "generator_users": generator_users,
                "assignments_num": len(generator_users),
                "STORES": BioVayaNoteCounterGenerator.STORES,
                "STATUES": BioVayaNoteCounterGenerator.STATUES,
            }
            if update_or_delete == "update":
                return render(request, 'assets_management/generator-update-form.html', context)
            if update_or_delete == "confirm_delete":
                context = {
                    "category": "generator",
                    "asset": generator,
                    "cancel_url_name": "assets_management:generator-detail",
                    "list_url": "assets_management:generators-list",
                    "asset_id": generator.asset_id,
                    "delete_url_name": "assets_management:generator-detail-update"
                }
                return render(request, 'assets_management/asking_delete_confirm.html', context)
            if update_or_delete == "delete":
                if self.delete(request, pk):
                    return redirect("assets_management:generators-list")
            return render(request, 'assets_management/generator-details.html', context)
        return redirect("assets_management:generators-list")

    def post(self, request, pk, update_or_delete="update", format=None):
        generator = self.get_object(pk)
        if generator:
            serializer = BioVayaNoteCounterGeneratorSerializer(data=request.POST, instance=generator, context={'request': request})
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"\n\nErrors: {serializer.errors}")
        return HttpResponseRedirect(reverse("assets_management:generator-detail", args=(pk,)))

    def delete(self, request, pk, format=None):
        generator = self.get_object(pk)
        if generator:
            generator.delete()
            return True
        return False


class AtmsList(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, report=None, *args, **kwargs):
        atms = Atm.objects.all().order_by('-recorded_date')
        context = {
            "atms": atms,
            "STORES": Atm.STORES,
            "STATUES": Atm.STATUES,
        }
        if report == 'report':
            filename = os.path.join("dashboard\\static\\reports\\atms.pdf")
            pdfkit.from_url("http://localhost:8000/report/atms/", filename, verbose=True, options=options)
            return FileResponse(open(filename, "rb"), content_type="application/pdf")
        return render(request, 'assets_management/atms-list.html', context)

    def post(self, request, *args, **kwargs):
        serializer = AtmSerializer(data=request.POST, context={'request': request})
        if serializer.is_valid():
            valid_tag_number = not is_asset_exist_with_tag_number(serializer.validated_data["tag_number"])
            valid_host_ip = not is_asset_exist_with_host_ip(serializer.validated_data["host_ip"])
            if valid_host_ip and valid_tag_number:
                print(f"\n\nVALID DATA: {serializer.validated_data}\n\n")
                serializer.save()
                print(f"\n\nVALID DATA: {serializer.data}\n\n")
            else:
                #some error messages
                if not valid_tag_number:
                    print(
                        f"\n\nTag number {serializer.data['tag_number']} already exists\n\n")
                if not valid_host_ip:
                    print(
                        f"\n\nHost IP {serializer.data['host_ip']} already exists\n\n")
        else:
            print(f"\n\nErrors: {serializer.errors}")
        return redirect("assets_management:atms-list")


class AtmDetail(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get_object(self, pk):
        try:
            return Atm.objects.get(asset_id=pk)
        except:
            return None

    def get(self, request, pk, update_or_delete=None, *args, **kwargs):
        atm = self.get_object(pk)
        atm_users = AssetAssignment.objects.filter(atm=atm, approval_status="Approved")
        maintenance_logs = MaintenanceLog.objects.filter(atm=atm)
        if atm:
            context = {
                "atm": atm,
                "atm_users": atm_users,
                "maintenance_logs": maintenance_logs,
                "assignments_num": len(atm_users),
                "maintenance_logs_num": len(maintenance_logs),
                "STORES": Atm.STORES,
                "STATUES": Atm.STATUES,
            }
            if update_or_delete == "update":
                return render(request, 'assets_management/atm-update-form.html', context)
            if update_or_delete == "confirm_delete":
                context = {
                    "category": "atm",
                    "asset": atm,
                    "cancel_url_name": "assets_management:atm-detail",
                    "list_url": "assets_management:atms-list",
                    "asset_id": atm.asset_id,
                    "delete_url_name": "assets_management:atm-detail-update"
                }
                return render(request, 'assets_management/asking_delete_confirm.html', context)
            if update_or_delete == "delete":
                if self.delete(request, pk):
                    return redirect("assets_management:atms-list")
            return render(request, 'assets_management/atm-details.html', context)
        return redirect("assets_management:atms-list")

    def post(self, request, pk, update_or_delete="update", format=None):
        atm = self.get_object(pk)
        if atm:
            serializer = AtmSerializer(data=request.POST, instance=atm, context={'request': request})
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"\n\nErrors: {serializer.errors}")
        return HttpResponseRedirect(reverse("assets_management:atm-detail", args=(pk,)))

    def delete(self, request, pk, format=None):
        atm = self.get_object(pk)
        if atm:
            atm.delete()
            return True
        return False


class SwitchesList(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, *args, **kwargs):
        switches = SwitchRouterFirewall.objects.filter(category="SWITCH").order_by('-recorded_date')

        context = {
            "switches": switches,
            "STORES": SwitchRouterFirewall.STORES,
            "STATUES": SwitchRouterFirewall.STATUES,
        }
        return render(request, 'assets_management/switches-list.html', context)

    def post(self, request, *args, **kwargs):
        serializer = SwitchRouterFirewallSerializer(data=request.POST, context={'request': request})
        if serializer.is_valid():
            valid_tag_number = not is_asset_exist_with_tag_number(serializer.validated_data["tag_number"])
            valid_host_ip = not is_asset_exist_with_host_ip(serializer.validated_data["host_ip"])
            if valid_host_ip and valid_tag_number:
                print(f"\n\nVALID DATA: {serializer.validated_data}\n\n")
                serializer.save()
                print(f"\n\nVALID DATA: {serializer.data}\n\n")
            else:
                #some error messages
                if not valid_tag_number:
                    print(
                        f"\n\nTag number {serializer.data['tag_number']} already exists\n\n")
                if not valid_host_ip:
                    print(
                        f"\n\nHost IP {serializer.data['host_ip']} already exists\n\n")
        else:
            print(f"\n\nErrors: {serializer.errors}")
        return redirect("assets_management:switches-list")


class SwitchDetail(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get_object(self, pk):
        try:
            return SwitchRouterFirewall.objects.get(asset_id=pk)
        except:
            return None

    def get(self, request, pk, update_or_delete=None, *args, **kwargs):
        switch = self.get_object(pk)
        switch_users = AssetAssignment.objects.filter(switch_router_firewall=switch, approval_status="Approved")
        if switch:
            context = {
                "switch": switch,
                "switch_users": switch_users,
                "assignments_num": len(switch_users),
                "STORES": SwitchRouterFirewall.STORES,
                "STATUES": SwitchRouterFirewall.STATUES,
            }
            if update_or_delete == "update":
                return render(request, 'assets_management/switch-update-form.html', context)
            if update_or_delete == "confirm_delete":
                context = {
                    "category": "switch",
                    "asset": switch,
                    "cancel_url_name": "assets_management:switch-detail",
                    "list_url": "assets_management:switches-list",
                    "asset_id": switch.asset_id,
                    "delete_url_name": "assets_management:switch-detail-update"
                }
                return render(request, 'assets_management/asking_delete_confirm.html', context)
            if update_or_delete == "delete":
                if self.delete(request, pk):
                    return redirect("assets_management:switches-list")
            return render(request, 'assets_management/switch-details.html', context)
        return redirect("assets_management:switches-list")

    def post(self, request, pk, update_or_delete="update", format=None):
        switch = self.get_object(pk)
        if switch:
            serializer = SwitchRouterFirewallSerializer(data=request.POST, instance=switch, context={'request': request})
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"\n\nErrors: {serializer.errors}")
        return HttpResponseRedirect(reverse("assets_management:switch-detail", args=(pk,)))

    def delete(self, request, pk, format=None):
        switch = self.get_object(pk)
        if switch:
            switch.delete()
            return True
        return False


class RoutersList(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, *args, **kwargs):
        routers = SwitchRouterFirewall.objects.filter(category="ROUTER").order_by('-recorded_date')
        context = {
            "routers": routers,
            "STORES": SwitchRouterFirewall.STORES,
            "STATUES": SwitchRouterFirewall.STATUES,
        }
        return render(request, 'assets_management/routers-list.html', context)

    def post(self, request, *args, **kwargs):
        serializer = SwitchRouterFirewallSerializer(data=request.POST, context={'request': request})
        if serializer.is_valid():
            valid_tag_number = not is_asset_exist_with_tag_number(serializer.validated_data["tag_number"])
            valid_host_ip = not is_asset_exist_with_host_ip(serializer.validated_data["host_ip"])
            if valid_host_ip and valid_tag_number:
                print(f"\n\nVALID DATA: {serializer.validated_data}\n\n")
                serializer.save()
                print(f"\n\nVALID DATA: {serializer.data}\n\n")
            else:
                #some error messages
                if not valid_tag_number:
                    print(
                        f"\n\nTag number {serializer.data['tag_number']} already exists\n\n")
                if not valid_host_ip:
                    print(
                        f"\n\nHost IP {serializer.data['host_ip']} already exists\n\n")
        else:
            print(f"\n\nErrors: {serializer.errors}")
        return redirect("assets_management:routers-list")


class RouterDetail(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get_object(self, pk):
        try:
            return SwitchRouterFirewall.objects.get(asset_id=pk)
        except:
            return None

    def get(self, request, pk, update_or_delete=None, *args, **kwargs):
        router = self.get_object(pk)
        router_users = AssetAssignment.objects.filter(switch_router_firewall=router, approval_status="Approved")
        if router:
            context = {
                "router": router,
                "router_users": router_users,
                "assignments_num": len(router_users),
                "STORES": SwitchRouterFirewall.STORES,
                "STATUES": SwitchRouterFirewall.STATUES,
            }
            if update_or_delete == "update":
                return render(request, 'assets_management/router-update-form.html', context)
            if update_or_delete == "confirm_delete":
                context = {
                    "category": "router",
                    "asset": router,
                    "cancel_url_name": "assets_management:router-detail",
                    "list_url": "assets_management:routers-list",
                    "asset_id": router.asset_id,
                    "delete_url_name": "assets_management:router-detail-update"
                }
                return render(request, 'assets_management/asking_delete_confirm.html', context)
            if update_or_delete == "delete":
                if self.delete(request, pk):
                    return redirect("assets_management:routers-list")
            return render(request, 'assets_management/router-details.html', context)
        return redirect("assets_management:routers-list")

    def post(self, request, pk, update_or_delete="update", format=None):
        router = self.get_object(pk)
        if router:
            serializer = SwitchRouterFirewallSerializer(
                data=request.POST, instance=router, context={'request': request})
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"\n\nErrors: {serializer.errors}")
        return HttpResponseRedirect(reverse("assets_management:router-detail", args=(pk,)))

    def delete(self, request, pk, format=None):
        router = self.get_object(pk)
        if router:
            router.delete()
            return True
        return False


class FirewallsList(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, *args, **kwargs):
        firewalls = SwitchRouterFirewall.objects.filter(category="FIREWALL").order_by('-recorded_date')
        context = {
            "firewalls": firewalls,
            "STORES": SwitchRouterFirewall.STORES,
            "STATUES": SwitchRouterFirewall.STATUES,
        }
        return render(request, 'assets_management/firewalls-list.html', context)

    def post(self, request, *args, **kwargs):
        serializer = SwitchRouterFirewallSerializer(data=request.POST, context={'request': request})
        if serializer.is_valid():
            valid_tag_number = not is_asset_exist_with_tag_number(serializer.validated_data["tag_number"])
            valid_host_ip = not is_asset_exist_with_host_ip(serializer.validated_data["host_ip"])
            if valid_host_ip and valid_tag_number:
                print(f"\n\nVALID DATA: {serializer.validated_data}\n\n")
                serializer.save()
                print(f"\n\nVALID DATA: {serializer.data}\n\n")
            else:
                #some error messages
                if not valid_tag_number:
                    print(
                        f"\n\nTag number {serializer.data['tag_number']} already exists\n\n")
                if not valid_host_ip:
                    print(
                        f"\n\nHost IP {serializer.data['host_ip']} already exists\n\n")
        else:
            print(f"\n\nErrors: {serializer.errors}")
        return redirect("assets_management:firewalls-list")


class FirewallDetail(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get_object(self, pk):
        try:
            return SwitchRouterFirewall.objects.get(asset_id=pk)
        except:
            return None

    def get(self, request, pk, update_or_delete=None, *args, **kwargs):
        firewall = self.get_object(pk)
        firewall_users = AssetAssignment.objects.filter(switch_router_firewall=firewall, approval_status="Approved")
        if firewall:
            context = {
                "firewall": firewall,
                "firewall_users": firewall_users,
                "assignments_num": len(firewall_users),
                "STORES": SwitchRouterFirewall.STORES,
                "STATUES": SwitchRouterFirewall.STATUES,
            }
            if update_or_delete == "update":
                return render(request, 'assets_management/firewall-update-form.html', context)
            if update_or_delete == "confirm_delete":
                context = {
                    "category": "firewall",
                    "asset": firewall,
                    "cancel_url_name": "assets_management:firewall-detail",
                    "list_url": "assets_management:firewalls-list",
                    "asset_id": firewall.asset_id,
                    "delete_url_name": "assets_management:firewall-detail-update"
                }
                return render(request, 'assets_management/asking_delete_confirm.html', context)
            if update_or_delete == "delete":
                if self.delete(request, pk):
                    return redirect("assets_management:firewalls-list")
            return render(request, 'assets_management/firewall-details.html', context)
        return redirect("assets_management:firewalls-list")

    def post(self, request, pk, update_or_delete="update", format=None):
        firewall = self.get_object(pk)
        if firewall:
            serializer = SwitchRouterFirewallSerializer(data=request.POST, instance=firewall, context={'request': request})
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"\n\nErrors: {serializer.errors}")
        return HttpResponseRedirect(reverse("assets_management:firewall-detail", args=(pk,)))

    def delete(self, request, pk, format=None):
        firewall = self.get_object(pk)
        if firewall:
            firewall.delete()
            return True
        return False


class PhysicalNodesList(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, *args, **kwargs):
        nodes = PhysicalNode.objects.all().order_by('-recorded_date')
        context = {
            "nodes": nodes,
            "STORES": PhysicalNode.STORES,
            "STATUES": PhysicalNode.STATUES,
        }
        return render(request, 'assets_management/nodes-list.html', context)

    def post(self, request, *args, **kwargs):
        serializer = PhysicalNodeSerializer(data=request.POST, context={'request': request})
        if serializer.is_valid():
            valid_tag_number = not is_asset_exist_with_tag_number(serializer.validated_data["tag_number"])
            valid_host_ip = not is_asset_exist_with_host_ip(serializer.validated_data["host_ip"])
            if valid_host_ip and valid_tag_number:
                print(f"\n\nVALID DATA: {serializer.validated_data}\n\n")
                serializer.save()
                print(f"\n\nVALID DATA: {serializer.data}\n\n")
            else:
                #some error messages
                if not valid_tag_number:
                    print(
                        f"\n\nTag number {serializer.data['tag_number']} already exists\n\n")
                if not valid_host_ip:
                    print(
                        f"\n\nHost IP {serializer.data['host_ip']} already exists\n\n")
        else:
            print(f"\n\nErrors: {serializer.errors}")
        return redirect("assets_management:nodes-list")


class PhysicalNodeDetail(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get_object(self, pk):
        try:
            return PhysicalNode.objects.get(asset_id=pk)
        except:
            return None

    def get(self, request, pk, update_or_delete=None, *args, **kwargs):
        node = self.get_object(pk)
        note_users = AssetAssignment.objects.filter(node=node, approval_status="Approved")
        if node:
            context = {
                "node": node,
                "note_users": note_users,
                "STORES": PhysicalNode.STORES,
                "STATUES": PhysicalNode.STATUES,
            }
            if update_or_delete == "update":
                return render(request, 'assets_management/node-update-form.html', context)
            if update_or_delete == "confirm_delete":
                context = {
                    "category": "physical node",
                    "asset": node,
                    "cancel_url_name": "assets_management:node-detail",
                    "list_url": "assets_management:nodes-list",
                    "asset_id": node.asset_id,
                    "delete_url_name": "assets_management:node-detail-update"
                }
                return render(request, 'assets_management/asking_delete_confirm.html', context)
            if update_or_delete == "delete":
                if self.delete(request, pk):
                    return redirect("assets_management:nodes-list")
            return render(request, 'assets_management/node-details.html', context)
        return redirect("assets_management:nodes-list")

    def post(self, request, pk, update_or_delete="update", format=None):
        node = self.get_object(pk)
        if node:
            serializer = PhysicalNodeSerializer(data=request.POST, instance=node, context={'request': request})
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"\n\nErrors: {serializer.errors}")
        return HttpResponseRedirect(reverse("assets_management:node-detail", args=(pk,)))

    def delete(self, request, pk, format=None):
        node = self.get_object(pk)
        if node:
            node.delete()
            return True
        return False


class SystemHostedApplicationsList(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, *args, **kwargs):
        applications = SystemHostedApplication.objects.all().order_by('-recorded_date')
        context = {
            "applications": applications,
        }
        return render(request, 'assets_management/applications-list.html', context)

    def post(self, request, *args, **kwargs):
        serializer = SystemHostedApplicationSerializer(data=request.POST, context={'request': request})
        if serializer.is_valid():
            valid_host_ip = not is_asset_exist_with_host_ip(serializer.validated_data["host_ip"])
            if valid_host_ip:
                print(f"\n\nVALID DATA: {serializer.validated_data}\n\n")
                serializer.save()
                print(f"\n\nVALID DATA: {serializer.data}\n\n")
            else:
                #some error messages
                if not valid_host_ip:
                    print(
                        f"\n\nHost IP {serializer.data['host_ip']} already exists\n\n")
        else:
            print(f"\n\nErrors: {serializer.errors}")
        return redirect("assets_management:applications-list")


class SystemHostedApplicationDetail(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get_object(self, pk):
        try:
            return SystemHostedApplication.objects.get(asset_id=pk)
        except:
            return None

    def get(self, request, pk, update_or_delete=None, *args, **kwargs):
        application = self.get_object(pk)
        if application:
            context = {
                "application": application,
                "STATUES": SystemHostedApplication.STATUES,
            }
            if update_or_delete == "update":
                return render(request, 'assets_management/application-update-form.html', context)
            if update_or_delete == "confirm_delete":
                context = {
                    "category": "hosted application",
                    "asset": application,
                    "cancel_url_name": "assets_management:application-detail",
                    "list_url": "assets_management:applications-list",
                    "asset_id": application.asset_id,
                    "delete_url_name": "assets_management:application-detail-update"
                }
                return render(request, 'assets_management/asking_delete_confirm.html', context)
            if update_or_delete == "delete":
                if self.delete(request, pk):
                    return redirect("assets_management:applications-list")
            return render(request, 'assets_management/application-details.html', context)
        return redirect("assets_management:applications-list")

    def post(self, request, pk, update_or_delete="update", format=None):
        application = self.get_object(pk)
        if application:
            serializer = SystemHostedApplicationSerializer(data=request.POST, instance=application, context={'request': request})
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"\n\nErrors: {serializer.errors}")
        return HttpResponseRedirect(reverse("assets_management:application-detail", args=(pk,)))

    def delete(self, request, pk, format=None):
        application = self.get_object(pk)
        if application:
            application.delete()
            return True
        return False