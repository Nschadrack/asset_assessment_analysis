from django.urls import path 
from .views import *

app_name = "requets_management"
urlpatterns = [
    path("requests/", RequetsList.as_view(), name="requests-list"),
    path("requests/<int:pk>/", RequestDetail.as_view(), name="request-detail"),
    path("requests/<int:pk>/<str:approve_or_reject>/", RequestDetail.as_view(), name="request-approve-reject"),
]
