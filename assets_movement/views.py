import re
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import View
from django.http.response import HttpResponse
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from users_management.models import User
from assets_management.models import (ComputerLapDeskTop, PrinterScanner, Screen, BioVayaNoteCounterGenerator,
                                      Atm, SwitchRouterFirewall, PhysicalNode, SystemHostedApplication)
from requests_management.models import RequestAssignment 
from .models import *




class ComputerAssignementView(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, computer_id=None, *args, **kwargs):
        all_users = User.objects.all().order_by("username")
        branches = Branch.objects.all().order_by("name")
        context = {
            "users": all_users,
            "branches": branches,
            "computer_id": computer_id,
        }
        if computer_id is not None:
            return render(request, "assets_movement/computer-assignment-form.html", context)  
        else:
            return HttpResponse("<h1>Hello there</h1>")
    
    def post(self, request, computer_id, *args, **kwargs):
        assignee_id = request.POST["assignee"].split("-")[0].strip()
        branch_name = request.POST["branch"].strip()
        exact_loc = request.POST["exact_location"].strip()
        require_move_ = request.POST["require_movement"]

        if require_move_.lower() == "on":
            require_move = True 
        else:
            require_move = False

        assignee = User.objects.filter(username=assignee_id).first()
        branch = Branch.objects.filter(name=branch_name).first()
        computer = ComputerLapDeskTop.objects.filter(asset_id=computer_id).first()
        assigner = request.user #current authenticated user

        if not assignee:
            #some messages, user does not exists
            pass
        if not branch:
            #some messages
            pass 

        if assignee and branch and computer:
            assignment = AssetAssignment(
                approver=assignee,
                assignee=assignee,
                assigner=assigner,
                branch=branch_name,
                exact_location=exact_loc,
                computer=computer,
                external_movement_required=require_move
            )
            assignment.save()
            request_assign = RequestAssignment(
                request_type="COMPUTER ASSIGNMENT",
                status="Pending",
                approver=assignment.approver,
                assignment_id=assignment,
                assigner=assignment.assigner
            )
            request_assign.save()
            
            return redirect(reverse("assets_management:computer-detail", args=(computer_id,)))
        else:
            return redirect(reverse("assets_movement:computer-assign", args=(computer_id,)))


class PrinterScannerAssignmentView(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, printer_id=None, *args, **kwargs):
        all_users = User.objects.all().order_by("username")
        branches = Branch.objects.all().order_by("name")
        printer = PrinterScanner.objects.filter(asset_id=printer_id).first()
        context = {
            "users": all_users,
            "branches": branches,
            "printer_id": printer_id,
            "printer_scanner": printer,
        }
        if printer_id is not None:
            return render(request, "assets_movement/printer-assignment-form.html", context)  
        else:
            return HttpResponse("<h1>Hello there</h1>")
    
    def post(self, request, printer_id, *args, **kwargs):
        approver_id = request.POST["approver"].split("-")[0].strip()
        branch_name = request.POST["branch"].strip()
        exact_loc = request.POST["exact_location"].strip()
        require_move_ = request.POST["require_movement"]

        if require_move_.lower() == "on":
            require_move = True 
        else:
            require_move = False

        approver = User.objects.filter(username=approver_id).first()
        branch = Branch.objects.filter(name=branch_name).first()
        printer = PrinterScanner.objects.filter(asset_id=printer_id).first()
        assigner = request.user #current authenticated user

        if not approver:
            #some messages, user does not exists
            pass
        if not branch:
            #some messages
            pass 

        if approver and branch and printer:
            assignment = AssetAssignment(
                approver=approver,
                assigner=assigner,
                branch=branch_name,
                exact_location=exact_loc,
                printer_scanner=printer,
                external_movement_required=require_move
            )
            assignment.save()
            request_assign = RequestAssignment(
                request_type="PRINTER/SCANNER ASSIGNMENT",
                status="Pending",
                approver=assignment.approver,
                assignment_id=assignment,
                assigner=assignment.assigner
            )
            request_assign.save()
            
            return redirect(reverse("assets_management:printer-detail", args=(printer_id,)))
        else:
            return redirect(reverse("assets_movement:printer-assign", args=(printer_id,)))



class ScreenAssignmentView(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, screen_id=None, *args, **kwargs):
        all_users = User.objects.all().order_by("username")
        branches = Branch.objects.all().order_by("name")
        context = {
            "users": all_users,
            "branches": branches,
            "screen_id": screen_id,
        }
        if screen_id is not None:
            return render(request, "assets_movement/screen-assignment-form.html", context)  
        else:
            return HttpResponse("<h1>Hello there</h1>")
    
    def post(self, request, screen_id, *args, **kwargs):
        approver_id = request.POST["assignee"].split("-")[0].strip()
        branch_name = request.POST["branch"].strip()
        exact_loc = request.POST["exact_location"].strip()
        require_move_ = request.POST["require_movement"]

        if require_move_.lower() == "on":
            require_move = True 
        else:
            require_move = False

        approver = User.objects.filter(username=approver_id).first()
        branch = Branch.objects.filter(name=branch_name).first()
        screen = Screen.objects.filter(asset_id=screen_id).first()
        assigner = request.user #current authenticated user

        if not approver:
            #some messages, user does not exists
            pass
        if not branch:
            #some messages
            pass 

        if approver and branch and screen:
            assignment = AssetAssignment(
                approver=approver,
                assignee=approver,
                assigner=assigner,
                branch=branch_name,
                exact_location=exact_loc,
                screen=screen,
                external_movement_required=require_move
            )
            assignment.save()
            request_assign = RequestAssignment(
                request_type="SCREEN ASSIGNMENT",
                status="Pending",
                approver=assignment.approver,
                assignment_id=assignment,
                assigner=assignment.assigner
            )
            request_assign.save()
            
            return redirect(reverse("assets_management:screen-detail", args=(screen_id,)))
        else:
            return redirect(reverse("assets_movement:screen-assign", args=(screen_id,)))


class BioAvayaAssignmentView(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, bio_avaya_id=None, *args, **kwargs):
        all_users = User.objects.all().order_by("username")
        branches = Branch.objects.all().order_by("name")
        bio_avaya = BioVayaNoteCounterGenerator.objects.filter(asset_id=bio_avaya_id).first()
        context = {
            "users": all_users,
            "branches": branches,
            "bio_avaya_id": bio_avaya_id,
            "bio_avaya": bio_avaya,
        }
        if bio_avaya_id is not None:
            return render(request, "assets_movement/bio-avaya-assignment-form.html", context)  
        else:
            return HttpResponse("<h1>Hello there</h1>")
    
    def post(self, request, bio_avaya_id, *args, **kwargs):
        approver_id = request.POST["assignee"].split("-")[0].strip()
        branch_name = request.POST["branch"].strip()
        exact_loc = request.POST["exact_location"].strip()
        require_move_ = request.POST["require_movement"]

        if require_move_.lower() == "on":
            require_move = True 
        else:
            require_move = False

        approver = User.objects.filter(username=approver_id).first()
        branch = Branch.objects.filter(name=branch_name).first()
        bio_avaya = BioVayaNoteCounterGenerator.objects.filter(asset_id=bio_avaya_id).first()
        assigner = request.user #current authenticated user

        if not approver:
            #some messages, user does not exists
            pass
        if not branch:
            #some messages
            pass 

        if approver and branch and bio_avaya:
            assignment = AssetAssignment(
                approver=approver,
                assignee=approver,
                assigner=assigner,
                branch=branch_name,
                exact_location=exact_loc,
                bio_avaya_note_gen=bio_avaya,
                external_movement_required=require_move
            )
            assignment.save()
            request_assign = RequestAssignment(
                request_type="BIO/AVAYA ASSIGNMENT",
                status="Pending",
                approver=assignment.approver,
                assignment_id=assignment,
                assigner=assignment.assigner
            )
            request_assign.save()
            
            if bio_avaya.category.upper() == "BIO":
                return redirect(reverse("assets_management:biometric-detail", args=(bio_avaya_id,)))
            else:
                return redirect(reverse("assets_management:avaya-detail", args=(bio_avaya_id,))) 
        else:
            return redirect(reverse("assets_movement:bio-avaya-assign", args=(bio_avaya_id,)))


class NoteCounterGeneratorAssignmentView(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, note_gen_id=None, *args, **kwargs):
        all_users = User.objects.all().order_by("username")
        branches = Branch.objects.all().order_by("name")
        note_gen = BioVayaNoteCounterGenerator.objects.filter(asset_id=note_gen_id).first()
        context = {
            "users": all_users,
            "branches": branches,
            "note_gen_id": note_gen_id,
            "note_gen": note_gen
        }
        if note_gen_id is not None:
            return render(request, "assets_movement/note-gen-assignment-form.html", context)  
        else:
            return HttpResponse("<h1>Hello there</h1>")
    
    def post(self, request, note_gen_id, *args, **kwargs):
        approver_id = request.POST["assignee"].split("-")[0].strip()
        branch_name = request.POST["branch"].strip()
        exact_loc = request.POST["exact_location"].strip()
        require_move_ = request.POST["require_movement"]

        if require_move_.lower() == "on":
            require_move = True 
        else:
            require_move = False

        approver = User.objects.filter(username=approver_id).first()
        branch = Branch.objects.filter(name=branch_name).first()
        note_gen = BioVayaNoteCounterGenerator.objects.filter(asset_id=note_gen_id).first()
        assigner = request.user #current authenticated user

        if not approver:
            #some messages, user does not exists
            pass
        if not branch:
            #some messages
            pass 

        if approver and branch and note_gen:
            assignment = AssetAssignment(
                approver=approver,
                assigner=assigner,
                branch=branch_name,
                exact_location=exact_loc,
                bio_avaya_note_gen=note_gen,
                external_movement_required=require_move
            )
            assignment.save()
            request_assign = RequestAssignment(
                request_type="NOTE COUNTER/GENERATOR ASSIGNMENT",
                status="Pending",
                approver=assignment.approver,
                assignment_id=assignment,
                assigner=assignment.assigner
            )
            request_assign.save()
            
            if note_gen.category.upper() == "GENERATOR":
                return redirect(reverse("assets_management:generator-detail", args=(note_gen_id,)))
            else:
                return redirect(reverse("assets_management:note-counter-detail", args=(note_gen_id,))) 
        else:
            return redirect(reverse("assets_movement:note-gen-assign", args=(note_gen_id,)))


class AtmAssignmentView(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, atm_id=None, *args, **kwargs):
        all_users = User.objects.all().order_by("username")
        branches = Branch.objects.all().order_by("name")
        context = {
            "users": all_users,
            "branches": branches,
            "atm_id": atm_id,
        }
        if atm_id is not None:
            return render(request, "assets_movement/atm-assignment-form.html", context)  
        else:
            return HttpResponse("<h1>Hello there</h1>")
    
    def post(self, request, atm_id, *args, **kwargs):
        approver_id = request.POST["assignee"].split("-")[0].strip()
        branch_name = request.POST["branch"].strip()
        exact_loc = request.POST["exact_location"].strip()
        require_move_ = request.POST["require_movement"]

        if require_move_.lower() == "on":
            require_move = True 
        else:
            require_move = False

        approver = User.objects.filter(username=approver_id).first()
        branch = Branch.objects.filter(name=branch_name).first()
        atm = Atm.objects.filter(asset_id=atm_id).first()
        assigner = request.user #current authenticated user

        if not approver:
            #some messages, user does not exists
            pass
        if not branch:
            #some messages
            pass 

        if approver and branch and atm:
            assignment = AssetAssignment(
                approver=approver,
                assigner=assigner,
                branch=branch_name,
                exact_location=exact_loc,
                atm=atm,
                external_movement_required=require_move
            )
            assignment.save()
            request_assign = RequestAssignment(
                request_type="ATM ASSIGNMENT",
                status="Pending",
                approver=assignment.approver,
                assignment_id=assignment,
                assigner=assignment.assigner
            )
            request_assign.save()
            
            return redirect(reverse("assets_management:atm-detail", args=(atm_id,)))
        else:
            return redirect(reverse("assets_movement:atm-assign", args=(atm_id,)))


class SwitchRouterFirewallAssignmentView(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, switch_router_firewall_id=None, *args, **kwargs):
        all_users = User.objects.all().order_by("username")
        branches = Branch.objects.all().order_by("name")
        switch_router_firewall = SwitchRouterFirewall.objects.filter(asset_id=switch_router_firewall_id).first()
        context = {
            "users": all_users,
            "branches": branches,
            "switch_router_firewall_id": switch_router_firewall_id,
            "switch_router_firewall": switch_router_firewall
        }
        if switch_router_firewall_id is not None:
            return render(request, "assets_movement/switch-router-firewall-assignment-form.html", context)  
        else:
            return HttpResponse("<h1>Hello there</h1>")
    
    def post(self, request, switch_router_firewall_id, *args, **kwargs):
        approver_id = request.POST["assignee"].split("-")[0].strip()
        branch_name = request.POST["branch"].strip()
        exact_loc = request.POST["exact_location"].strip()
        require_move_ = request.POST["require_movement"]

        if require_move_.lower() == "on":
            require_move = True 
        else:
            require_move = False

        approver = User.objects.filter(username=approver_id).first()
        branch = Branch.objects.filter(name=branch_name).first()
        switch_router_firewall = SwitchRouterFirewall.objects.filter(asset_id=switch_router_firewall_id).first()
        assigner = request.user #current authenticated user

        if not approver:
            #some messages, user does not exists
            pass
        if not branch:
            #some messages
            pass 

        if approver and branch and switch_router_firewall:
            assignment = AssetAssignment(
                approver=approver,
                assigner=assigner,
                branch=branch_name,
                exact_location=exact_loc,
                switch_router_firewall=switch_router_firewall,
                external_movement_required=require_move
            )
            assignment.save()
            request_assign = RequestAssignment(
                request_type="SWITCH/ROUTER/FIREWALL ASSIGNMENT",
                status="Pending",
                approver=assignment.approver,
                assignment_id=assignment,
                assigner=assignment.assigner
            )
            request_assign.save()
            
            if switch_router_firewall.category.upper() == "SWITCH":
                return redirect(reverse("assets_management:switch-detail", args=(switch_router_firewall_id,)))
            elif switch_router_firewall.category.upper() == "ROUTER":
                return redirect(reverse("assets_management:router-detail", args=(switch_router_firewall_id,)))
            else:
                return redirect(reverse("assets_management:firewall-detail", args=(switch_router_firewall_id,))) 
        else:
            return redirect(reverse("assets_movement:switch-router-firewall-assign", args=(switch_router_firewall_id,)))


class ServerAssignmentView(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"
    def get(self, request, node_id=None, *args, **kwargs):
        all_users = User.objects.all().order_by("username")
        branches = Branch.objects.all().order_by("name")
        context = {
            "users": all_users,
            "branches": branches,
            "node_id": node_id,
        }
        if node_id is not None:
            return render(request, "assets_movement/node-assignment-form.html", context)  
        else:
            return HttpResponse("<h1>Hello there</h1>")
    
    def post(self, request, node_id, *args, **kwargs):
        approver_id = request.POST["assignee"].split("-")[0].strip()
        branch_name = request.POST["branch"].strip()
        exact_loc = request.POST["exact_location"].strip()
        require_move_ = request.POST["require_movement"]

        if require_move_.lower() == "on":
            require_move = True 
        else:
            require_move = False

        approver = User.objects.filter(username=approver_id).first()
        branch = Branch.objects.filter(name=branch_name).first()
        node = PhysicalNode.objects.filter(asset_id=node_id).first()
        assigner = request.user #current authenticated user

        if not approver:
            #some messages, user does not exists
            pass
        if not branch:
            #some messages
            pass 

        if approver and branch and node:
            assignment = AssetAssignment(
                approver=approver,
                assigner=assigner,
                branch=branch_name,
                exact_location=exact_loc,
                node=node,
                external_movement_required=require_move
            )
            assignment.save()
            request_assign = RequestAssignment(
                request_type="SERVER ASSIGNMENT",
                status="Pending",
                approver=assignment.approver,
                assignment_id=assignment,
                assigner=assignment.assigner
            )
            request_assign.save()           
            
            return redirect(reverse("assets_management:node-detail", args=(node_id,)))
        else:
            return redirect(reverse("assets_movement:node-assign", args=(node_id,)))

