from rest_framework import serializers

from .models import (ComputerLapDeskTop, PrinterScanner, Screen, BioVayaNoteCounterGenerator, 
                    Atm, SwitchRouterFirewall, PhysicalNode, SystemHostedApplication)


def return_model_fields(model):
    fields = []
    fields.extend([field.name for field in model._meta.get_fields()])

    return fields

class BuildCommonAttributeInstance:
    """
    The class which builds instance with some attributes changed and updated them with data 
    in validated data passed in
    """
    def __init__(self, instance, validated_data) -> None:
        self.__instance = instance
        self.__validated_data = validated_data
    
    def build_instance(self):
        self.__instance.serial_number = self.__validated_data.get('serial_number', self.__instance.serial_number)
        self.__instance.model = self.__validated_data.get('model', self.__instance.model)
        self.__instance.tag_number = self.__validated_data.get('tag_number', self.__instance.tag_number)
        self.__instance.purchase_price = self.__validated_data.get('purchase_price', self.__instance.purchase_price)
        self.__instance.entry_date_in_bank = self.__validated_data.get('entry_date_in_bank', self.__instance.entry_date_in_bank)
        self.__instance.warranty_time = self.__validated_data.get('warranty_time', self.__instance.warranty_time)
        self.__instance.lifetime = self.__validated_data.get('lifetime', self.__instance.lifetime)
        self.__instance.which_store = self.__validated_data.get('which_store', self.__instance.which_store)
        self.__instance.asset_sold = self.__validated_data.get('asset_sold', self.__instance.asset_sold)
        self.__instance.sold_date = self.__validated_data.get('sold_date', self.__instance.sold_date)
        self.__instance.sale_price = self.__validated_data.get('sale_price', self.__instance.sale_price)
        self.__instance.set_status(self.__validated_data.get('status', self.__instance.status))

        return self.__instance


class ComputerLapDeskTopSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComputerLapDeskTop
        fields = return_model_fields(ComputerLapDeskTop)

    def create(self, validated_data):
        assignments = validated_data["computer_assignments"]
        validated_data.pop("computer_assignments")
        computer = ComputerLapDeskTop.objects.create(**validated_data)
        computer.computer_assignments.set(assignments)
        return computer
        
    
    def update(self, instance, validated_data):
        
        common_attr = BuildCommonAttributeInstance(instance=instance, validated_data=validated_data)
        instance = common_attr.build_instance()

        instance.hostname = validated_data.get('hostname', instance.hostname)
        instance.category = validated_data.get('category', instance.category)
        instance.storage_type = validated_data.get('storage_type', instance.storage_type)
        instance.harddisk_size = validated_data.get('harddisk_size', instance.harddisk_size)
        instance.ssd_size = validated_data.get('ssd_size', instance.ssd_size)
        instance.harddisk_measure = validated_data.get('harddisk_measure', instance.harddisk_measure)
        instance.ssd_measure = validated_data.get('ssd_measure', instance.ssd_measure)
        instance.memory_size = validated_data.get('memory_size', instance.memory_size)
        instance.memory_measure = validated_data.get('memory_measure', instance.memory_measure)
        instance.processor_manufacturer = validated_data.get('processor_manufacturer', instance.processor_manufacturer)
        instance.processor_type = validated_data.get('processor_type', instance.processor_type)
        instance.process_speed = validated_data.get('process_speed', instance.process_speed)
        instance.processor_speed_measure = validated_data.get('processor_speed_measure', instance.processor_speed_measure)
        instance.processor_name = validated_data.get('processor_name', instance.processor_name)

        instance.symantic_installed = validated_data.get('symantic_installed', instance.symantic_installed)

        instance.os_installed = validated_data.get('os_installed', instance.os_installed)

        instance.save()

        return instance
    

class PrinterScannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrinterScanner
        fields = return_model_fields(PrinterScanner)
    
    def create(self, validated_data):
        assignments = validated_data["printer_scanner_assignments"]
        validated_data.pop("printer_scanner_assignments")
        printer = PrinterScanner.objects.create(**validated_data)
        printer.printer_scanner_assignments.set(assignments)
        return printer
   
    def update(self, instance, validated_data):
        common_attr = BuildCommonAttributeInstance(instance=instance, validated_data=validated_data)
        instance = common_attr.build_instance()

        instance.category = validated_data.get('category', instance.category)
        instance.category_type = validated_data.get('category_type', instance.category_type)
        instance.other_type_name = validated_data.get('other_type_name', instance.other_type_name)
        instance.connection_type = validated_data.get('connection_type', instance.connection_type)
        instance.host_ip = validated_data.get('host_ip', instance.host_ip)
        instance.version = validated_data.get('version', instance.version)
    
        instance.save()

        return instance


class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen 
        fields = return_model_fields(Screen)
    
    def create(self, validated_data):
        assignments = validated_data["screen_assignments"]
        validated_data.pop("screen_assignments")
        screen = Screen.objects.create(**validated_data)
        screen.screen_assignments.set(assignments)
        return screen

    def update(self, instance, validated_data):
        common_attr = BuildCommonAttributeInstance(instance=instance, validated_data=validated_data)
        instance = common_attr.build_instance()

        instance.category = validated_data.get('category', instance.category)
        instance.size = validated_data.get('size', instance.size)
        instance.size_measure = validated_data.get('size_measure', instance.size_measure)

        instance.save()

        return instance


class BioVayaNoteCounterGeneratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BioVayaNoteCounterGenerator
        fields = return_model_fields(BioVayaNoteCounterGenerator)
    
    def create(self, validated_data):
        assignments = validated_data["bio_avaya_note_gen_assignments"]
        validated_data.pop("bio_avaya_note_gen_assignments")
        bio = BioVayaNoteCounterGenerator.objects.create(**validated_data)
        bio.bio_avaya_note_gen_assignments.set(assignments)
        return bio

    def update(self, instance, validated_data):
        common_attr = BuildCommonAttributeInstance(instance=instance, validated_data=validated_data)
        instance = common_attr.build_instance()

        instance.category = validated_data.get('category', instance.category)
        instance.version = validated_data.get('version', instance.version)

        instance.save()

        return instance


class AtmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atm 
        fields = return_model_fields(Atm)
    
    def create(self, validated_data):
        assignments = validated_data["atm_assignments"]
        validated_data.pop("atm_assignments")
        atm = Atm.objects.create(**validated_data)
        atm.atm_assignments.set(assignments)
        return atm

    def update(self, instance, validated_data):
        common_attr = BuildCommonAttributeInstance(instance=instance, validated_data=validated_data)
        instance = common_attr.build_instance()

        instance.hostname = validated_data.get('hostname', instance.hostname)
        instance.os_installed = validated_data.get('os_installed', instance.os_installed)

        instance.add_usage_start_date(validated_data.get('usage_start_date', instance.usage_start_date))

        instance.host_ip = validated_data.get('host_ip', instance.host_ip)
        instance.version = validated_data.get('version', instance.version)

        instance.save()

        return instance


class SwitchRouterFirewallSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwitchRouterFirewall
        fields = return_model_fields(SwitchRouterFirewall)

    def create(self, validated_data):
        assignments = validated_data["switch_router_frewall_assignments"]
        validated_data.pop("switch_router_frewall_assignments")
        router = SwitchRouterFirewall.objects.create(**validated_data)
        router.switch_router_frewall_assignments.set(assignments)
        return router

    def update(self, instance, validated_data):
        common_attr = BuildCommonAttributeInstance(instance=instance, validated_data=validated_data)
        instance = common_attr.build_instance()

        instance.hostname = validated_data.get('hostname', instance.hostname)
        instance.host_ip = validated_data.get('host_ip', instance.host_ip)
        instance.category = validated_data.get('category', instance.category)
        instance.manufacturer = validated_data.get('manufacturer', instance.manufacturer)
        instance.version = validated_data.get('version', instance.version)

        instance.add_usage_start_date(validated_data.get('usage_start_date', instance.usage_start_date))

        instance.save()

        return instance


class PhysicalNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalNode
        fields = return_model_fields(PhysicalNode)
    
    def create(self, validated_data):
        assignments = validated_data["node_assignments"]
        validated_data.pop("node_assignments")
        node = PhysicalNode.objects.create(**validated_data)
        node.node_assignments.set(assignments)
        return node
    
    def update(self, instance, validated_data):
        common_attr = BuildCommonAttributeInstance(instance=instance, validated_data=validated_data)
        instance = common_attr.build_instance()

        instance.hostname = validated_data.get('hostname', instance.hostname)
        instance.host_ip = validated_data.get('host_ip', instance.host_ip)
        instance.vendor = validated_data.get('vendor', instance.vendor)
        instance.role = validated_data.get('role', instance.role)
        instance.os_installed = validated_data.get('os_installed', instance.os_installed)
        instance.installation_year = validated_data.get('installation_year', instance.installation_year)

        instance.add_usage_start_date(validated_data.get('usage_start_date', instance.usage_start_date))
        instance.save()

        return instance


class SystemHostedApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemHostedApplication
        fields = return_model_fields(SystemHostedApplication)
    
    def create(self,  validated_data):
        assignments = validated_data["application_assignments"]
        validated_data.pop("application_assignments")
        application = SystemHostedApplication.objects.create(**validated_data)
        application.application_assignments.set(assignments)
        return application

    def update(self, instance, validated_data):
        instance.serial_number = validated_data.get('serial_number', instance.serial_number)
        instance.model = validated_data.get('model', instance.model)
        instance.supporting_time = validated_data.get('supporting_time', instance.supporting_time)
        instance.in_use = validated_data.get('in_use', instance.in_use)
        instance.hostname = validated_data.get('hostname', instance.hostname)
        instance.host_ip = validated_data.get('host_ip', instance.host_ip)
        instance.role = validated_data.get('role', instance.role)
        instance.os_installed = validated_data.get('os_installed', instance.os_installed)
        instance.installation_year = validated_data.get('installation_year', instance.installation_year)
        self.instance.set_status(validated_data.get('status', self.instance.status))
        instance.usage_start_date = validated_data.get('usage_start_date', instance.usage_start_date)
        instance.save()

        return instance
