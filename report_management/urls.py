from django.urls import path 
from . views import *

app_name = "report_management"

urlpatterns = [
    path("computers/", ComputersListReport.as_view(), name='report-computers'),
    path("dashboard/", dashboard_report, name="dashboard-report"),
    path("printers/", PrintersListReport.as_view(), name="printers-report"),
    path("scanners/", ScannersListReport.as_view(), name="scanners-report"),
    path("note-counters/", NoteCountersListReport.as_view(), name="note-counters-report"),
    path("atms/", AtmsListReport.as_view(), name="report-atm"),
]
