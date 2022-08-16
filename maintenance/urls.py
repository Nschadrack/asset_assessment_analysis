from django.urls import path 
from .views import MaintenanceLogList, SparepartList, MaintenanceLogDetail

app_name = 'maintenance'

urlpatterns = [
    path('<int:asset_id>/<str:category>/recording/', MaintenanceLogList.as_view(), name='maintenance-list'),
    path('maintenance-log-details/<int:maintenance_id>/', MaintenanceLogDetail.as_view(), name='maintenance-detail'),
    path('spareparts-list/', SparepartList.as_view(), name="spareparts-list"),
]
