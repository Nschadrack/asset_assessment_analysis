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


class PrinterScannerAssignmentView(View):
    pass