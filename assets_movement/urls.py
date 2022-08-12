from django.urls import path 
from .views import *

app_name = "assets_movement"

urlpatterns = [
    path("computers/", ComputerAssignementView.as_view(), name="computers-assign-list"),
    path("computers/<int:computer_id>/assignment/", ComputerAssignementView.as_view(), name="computer-assign"),
    path("printers/", PrinterScannerAssignmentView.as_view(), name="printers-assign-list"),
    path("printers/<int:printer_id>/assignment/", PrinterScannerAssignmentView.as_view(), name="printer-assign"),
    path("screens/", ScreenAssignmentView.as_view(), name="screen-assign-list"),
    path("screens/<int:screen_id>/assignment/", ScreenAssignmentView.as_view(), name="screen-assign"),
    path("biometric-avaya/", BioAvayaAssignmentView.as_view(), name="bio-avaya-assign-list"),
    path("biometric-avaya/<int:bio_avaya_id>/assignment/", BioAvayaAssignmentView.as_view(), name="bio-avaya-assign"),
    path("note-counter-generator/", NoteCounterGeneratorAssignmentView.as_view(), name="note-gen-assign-list"),
    path("note-counter-generator/<int:note_gen_id>/assignment/", NoteCounterGeneratorAssignmentView.as_view(), name="note-gen-assign"),
    path("atms/", AtmAssignmentView.as_view(), name="atm-assign-list"),
    path("atms/<int:atm_id>/assignment/", AtmAssignmentView.as_view(), name="atm-assign"),
    path("switch-router-firewall/", SwitchRouterFirewallAssignmentView.as_view(), name="switch-router-firewall-assign-list"),
    path("switch-router-firewall/<int:switch_router_firewall_id>/assignment/", SwitchRouterFirewallAssignmentView.as_view(), name="switch-router-firewall-assign"),
    path("servers/", ServerAssignmentView.as_view(), name="node-assign-list"),
    path("servers/<int:node_id>/assignment/", ServerAssignmentView.as_view(), name="node-assign"),
]
