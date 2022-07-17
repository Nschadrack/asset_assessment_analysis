from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url="account:index", redirect_field_name="redirect_to")
def dashboard(request):

    return render(request, 'dashboard/dashboard.html')


