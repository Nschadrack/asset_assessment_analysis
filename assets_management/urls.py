from django.urls import path 


from .views import *

app_name = 'assets_management'

urlpatterns = [ 
    path('computers/', ComputersList.as_view(), name='computers-list'),
    path('computers/<int:pk>/', ComputerDetail.as_view(), name='computer-detail'),
    path('computers/<int:pk>/<str:update_or_delete>/',ComputerDetail.as_view(), name='computer-detail-update'),

    path('printers/', PrintersList.as_view(), name='printers-list'),
    path('printers/<int:pk>/', PrinterDetail.as_view(), name='printer-detail'),
    path('printers/<int:pk>/<str:update_or_delete>/', PrinterDetail.as_view(), name='printer-detail-update'),

    path('scanners/', ScannersList.as_view(), name='scanners-list'),
    path('scanners/<int:pk>/', ScannerDetail.as_view(), name='scanner-detail'),
    path('scanners/<int:pk>/<str:update_or_delete>/', ScannerDetail.as_view(), name='scanner-detail-update'),

    path('screens/', ScreensList.as_view(), name='screens-list'),
    path('screens/<int:pk>/', ScreenDetail.as_view(), name='screen-detail'),
    path('screens/<int:pk>/<str:update_or_delete>/', ScreenDetail.as_view(), name='screen-detail-update'),

    path('biometrics/', BiometricsList.as_view(), name='biometrics-list'),
    path('biometrics/<int:pk>/', BiometricDetail.as_view(), name='biometric-detail'),
    path('biometrics/<int:pk>/<str:update_or_delete>/', BiometricDetail.as_view(), name='biometric-detail-update'),

    path('avaya/', AvayaList.as_view(), name='avaya-list'),
    path('avaya/<int:pk>/', AvayaDetail.as_view(), name='avaya-detail'),
    path('avaya/<int:pk>/<str:update_or_delete>/', AvayaDetail.as_view(), name='avaya-detail-update'),
    
    path('note-counters/', NoteCountersList.as_view(), name='note-counters-list'),
    path('note-counters/<int:pk>/', NoteCounterDetail.as_view(), name='note-counter-detail'),
    path('note-counters/<int:pk>/<str:update_or_delete>/', NoteCounterDetail.as_view(), name='note-counter-detail-update'),

    path('generators/', GeneratorsList.as_view(), name='generators-list'),
    path('generators/<int:pk>/', GeneratorDetail.as_view(), name='generator-detail'),
    path('generators/<int:pk>/<str:update_or_delete>/', GeneratorDetail.as_view(), name='generator-detail-update'),

    path('atms/', AtmsList.as_view(), name='atms-list'),
    path('atms/<int:pk>/', AtmDetail.as_view(), name='atm-detail'),
    path('atms/<int:pk>/<str:update_or_delete>/', AtmDetail.as_view(), name='atm-detail-update'),

    path('switches/', SwitchesList.as_view(), name='switches-list'),
    path('switches/<int:pk>/', SwitchDetail.as_view(), name='switch-detail'),
    path('switches/<int:pk>/<str:update_or_delete>/', SwitchDetail.as_view(), name='switch-detail-update'),

    path('routers/', RoutersList.as_view(), name='routers-list'),
    path('routers/<int:pk>/', RouterDetail.as_view(), name='router-detail'),
    path('routers/<int:pk>/<str:update_or_delete>/', RouterDetail.as_view(), name='router-detail-update'),

    path('firewalls/', FirewallsList.as_view(), name='firewalls-list'),
    path('firewalls/<int:pk>/', FirewallDetail.as_view(), name='firewall-detail'),
    path('firewalls/<int:pk>/<str:update_or_delete>/', FirewallDetail.as_view(), name='firewall-detail-update'),

    path('physical-nodes/', PhysicalNodesList.as_view(), name='nodes-list'),
    path('node-servers/<int:pk>/', PhysicalNodeDetail.as_view(), name='node-detail'),
    path('node-servers/<int:pk>/<str:update_or_delete>/', PhysicalNodeDetail.as_view(), name='node-detail-update'),

    path('system-hosted-applications/', SystemHostedApplicationsList.as_view(), name='applications-list'),
    path('system-application-hosted/<int:pk>/', SystemHostedApplicationDetail.as_view(), name='application-detail'),
    path('system-application-hosted/<int:pk>/<str:update_or_delete>/', SystemHostedApplicationDetail.as_view(), name='application-detail-update'),
]


