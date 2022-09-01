from django.urls import path

from .views import *

app_name = 'dashboard'
urlpatterns = [
    path("overall/", dashboard, name='overall'),
    path("overall/<str:report>/", dashboard, name='overall-report'),
 ]