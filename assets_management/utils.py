from .models import *

def is_asset_exist_with_host_ip(host_ip):
    models_ =  (PrinterScanner, 
                Atm, 
                SwitchRouterFirewall, 
                PhysicalNode, 
                SystemHostedApplication)
    host_ip = host_ip.strip()
    if len(host_ip) > 0:
        for model in models_:
            found_asset = model.objects.filter(host_ip=host_ip)
            if len(found_asset)>0:
                return True
    return False


def is_asset_exist_with_tag_number(tag_number):
    models_ = (ComputerLapDeskTop,
               PrinterScanner,
               Screen,
               BioVayaNoteCounterGenerator,
               Atm,
               SwitchRouterFirewall,
               PhysicalNode)
    tag_number = tag_number.strip()
    if len(tag_number) >0:
        for model in models_:
            found_asset = model.objects.filter(tag_number=tag_number)
            if len(found_asset)>0:
                return True 
    return False