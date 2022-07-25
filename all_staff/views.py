from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from assets_movement.models import AssetAssignment



@login_required(login_url="account:index", redirect_field_name="redirect_to")
def general_board(request):
    return render(request, "all_staff/general-board.html")


@login_required(login_url="account:index", redirect_field_name="redirect_to")
def user_computers_list(request):
    user = request.user 
    computer_users = AssetAssignment.objects.filter(approver=user, approval_status="Approved").exclude(computer=None)
    assignments_num = AssetAssignment.objects.filter(approver=user, approval_status="Approved").exclude(computer=None).all().count()
    context = {
        "computer_users": computer_users,
        "assignments_num": assignments_num,
    }
    return render(request, "all_staff/computers-assigned-to-me.html", context)
