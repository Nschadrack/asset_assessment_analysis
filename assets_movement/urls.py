from django.urls import path 
from .views import *

app_name = "assets_movement"

urlpatterns = [
    path("computers/", ComputerAssignementView.as_view(), name="computers-assign-list"),
    path("computers/<int:computer_id>/assignment/", ComputerAssignementView.as_view(), name="computer-assign"),
]
