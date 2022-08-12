from django.urls import path 
from .views import MaintenanceLogList

app_name = 'maintenance'
urlpatterns = [
    path('<int:asset_id>/<str:category>/recording/', MaintenanceLogList.as_view(), name='maintenance-list'),
]
