from django.urls import path 
from .views import *

app_name = "requets_management"
urlpatterns = [
    path("requests/general", RequetsList.as_view(), name="requests-list"),
    path("requests/general/<int:pk>/", RequestDetail.as_view(), name="request-detail"),
    path("requests/general/<int:pk>/<str:approve_or_reject>/", RequestDetail.as_view(), name="request-approve-reject"),

    path("requests/", RequetsListAdmin.as_view(), name="requests-admin-list"),
    path("requests/<int:pk>/", RequestDetailAdmin.as_view(), name="request-admin-detail"),
    path("requests/<int:pk>/<str:view_or_delete>/", RequestDetailAdmin.as_view(), name="request-view-or-delete"),
]
