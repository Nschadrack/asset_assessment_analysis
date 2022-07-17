from django.contrib import admin
from .serializers import return_model_fields

from .models import (ComputerLapDeskTop, PrinterScanner, Screen, BioVayaNoteCounterGenerator, 
                    Atm, SwitchRouterFirewall, PhysicalNode, SystemHostedApplication)

admin.site.register(ComputerLapDeskTop)
admin.site.register(PrinterScanner)
admin.site.register(Screen)
admin.site.register(BioVayaNoteCounterGenerator)
admin.site.register(Atm)
admin.site.register(SwitchRouterFirewall)
admin.site.register(PhysicalNode)
admin.site.register(SystemHostedApplication)

# print(f"\n\nATM Fields: {return_model_fields(Atm)}\n\n")

