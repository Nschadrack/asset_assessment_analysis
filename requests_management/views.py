from datetime import datetime
from django.shortcuts import render, redirect
from django.views import View 
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from assets_movement.models import AssetAssignment


class RequetsList(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"

    def get(self, request, *args, **kwargs):
        user = request.user
        requests = RequestAssignment.objects.filter(approver=user, status="Pending").order_by("-opened_date")
        context = {
            "requests": requests,
            "requests_num": len(requests),
        }
        return render(request, "requests_management/requests-list.html", context)

    def post(self, request, *args, **kwargs):
        pass


class RequestDetail(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"

    def get(self, request, pk, approve_or_reject=None, *args, **kwargs):
        requet = RequestAssignment.objects.filter(pk=pk).first()
        assign = AssetAssignment.objects.get(pk=requet.assignment_id.assignment_num)
        context = {
            "requet": requet,
            "assign": assign,
        }

        if approve_or_reject == "approve":
            assign.status = "Active"
            requet.status = "Approved"
            assign.approval_status = "Approved"
            assign.date_approved = datetime.now()
            if assign.computer is not None:
                assign.computer.current_location = assign.branch
                assign.computer.currect_exact_loc = assign.exact_location 
                assign.computer.in_store = False 
                assign.computer.which_store = "NOT-IN-STORE"
                assign.computer.in_use = True
                assign.computer.save() 

            elif assign.printer_scanner is not None:
                assign.printer_scanner.current_location = assign.branch
                assign.printer_scanner.currect_exact_loc = assign.exact_location 
                assign.printer_scanner.in_store = False 
                assign.printer_scanner.which_store = "NOT-IN-STORE"
                assign.printer_scanner.in_use = True
                assign.printer_scanner.save() 

            elif assign.screen is not None:
                assign.screen.current_location = assign.branch
                assign.screen.currect_exact_loc = assign.exact_location 
                assign.screen.in_store = False 
                assign.screen.which_store = "NOT-IN-STORE"
                assign.screen.in_use = True
                assign.screen.save() 
            
            elif assign.bio_avaya_note_gen is not None:
                assign.bio_avaya_note_gen.current_location = assign.branch
                assign.bio_avaya_note_gen.currect_exact_loc = assign.exact_location 
                assign.bio_avaya_note_gen.in_store = False 
                assign.bio_avaya_note_gen.which_store = "NOT-IN-STORE"
                assign.bio_avaya_note_gen.in_use = True
                assign.bio_avaya_note_gen.save() 

            elif assign.atm is not None:
                assign.atm.current_location = assign.branch
                assign.atm.currect_exact_loc = assign.exact_location 
                assign.atm.in_store = False 
                assign.atm.which_store = "NOT-IN-STORE"
                assign.atm.in_use = True
                assign.atm.save() 
            
            elif assign.switch_router_firewall is not None:
                assign.switch_router_firewall.current_location = assign.branch
                assign.switch_router_firewall.currect_exact_loc = assign.exact_location 
                assign.switch_router_firewall.in_store = False 
                assign.switch_router_firewall.which_store = "NOT-IN-STORE"
                assign.switch_router_firewall.in_use = True
                assign.switch_router_firewall.save()
            
            elif assign.node is not None:
                assign.node.current_location = assign.branch
                assign.node.currect_exact_loc = assign.exact_location 
                assign.node.in_store = False 
                assign.node.which_store = "NOT-IN-STORE"
                assign.node.in_use = True
                assign.node.save()

            assign.save()
            requet.save()
            return redirect("requests_management:requests-list")
        elif approve_or_reject == "reject":
            return render(request, "requests_management/rejection-note.html")
        else:
            return render(request, "requests_management/request-details.html", context) 

    def post(self, request, pk, approve_or_reject="reject", *args, **kwargs):
        requet = RequestAssignment.objects.filter(pk=pk).first()
        assign = AssetAssignment.objects.get(pk=requet.assignment_id.assignment_num)
        requet.status = "Rejected"
        requet.rejection_note = request.POST["rejection_note"].strip() 
        assign.approval_status = "Rejected"
        assign.status = "Inactive"
        assign.date_approved = datetime.now()
        assign.save()
        requet.save()

        if requet.request_type == "COMPUTER ASSIGNMENT":
            return redirect("all_staff:user-computers")

        return redirect("all_staff:overall")


class RequetsListAdmin(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"

    def get(self, request, *args, **kwargs):
        user = request.user
        requests = RequestAssignment.objects.filter(assigner=user).order_by("-opened_date")
        context = {
            "requests": requests,
            "requests_num": len(requests),
        }
        return render(request, "requests_management/requests-admin-list.html", context)

    def post(self, request, *args, **kwargs):
        pass


class RequestDetailAdmin(LoginRequiredMixin, View):
    login_url = "account:index"
    redirect_field_name = "redirect_to"

    def get(self, request, pk, view_or_delete=None, *args, **kwargs):
        requet = RequestAssignment.objects.filter(pk=pk).first()
        assign = AssetAssignment.objects.get(pk=requet.assignment_id.assignment_num)
        context = {
            "requet": requet,
            "assign": assign,
        }

        if view_or_delete == "delete":
            assign.delete()
            return redirect("dashboard:overall")
        else:
            return render(request, "requests_management/request-admin-details.html", context) 

