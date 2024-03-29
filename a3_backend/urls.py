"""a3_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('account.urls', namespace='account')),
    path('', include('all_staff.urls', namespace='all_staff')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('assets_management/', include('assets_management.urls', namespace='assets_management')),
    path('users_management/', include('users_management.urls', namespace='users_management')),
    path('assets_consolidation', include('assets_movement.urls', namespace='assets_movement')),
    path('requests_management/', include('requests_management.urls', namespace='requests_management')),
    path('maintenance_log/', include('maintenance.urls', namespace='maintenance')),
    path('report/', include('report_management.urls', namespace='report_management')),
]
