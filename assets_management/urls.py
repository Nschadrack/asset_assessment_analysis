from django.urls import path 

from .views import *

app_name = 'assets_management'

urlpatterns = [ 
    path('computers/', ComputerList.as_view(), name='computers_list'),
    path('computers/<int:pk>/', ComputerDetail.as_view(), name='computer-detail'),
]