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
            assign.save()
            requet.save()
            return redirect("dashboard:overall")
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
        assign.save()
        requet.save()

        return redirect("dashboard:overall")