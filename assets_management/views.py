from django.shortcuts import render

from .models import (ComputerLapDeskTop, PrinterScanner, Screen, BioVayaNoteCounterGenerator,
                     Atm, SwitchRouterFirewall, PhysicalNode, SystemHostedApplication)
from .serializers import (ComputerLapDeskTopSerializer, PrinterScannerSerializer, ScreenSerializer, BioVayaNoteCounterGeneratorSerializer, AtmSerializer,
                          SwitchRouterFirewallSerializer, PhysicalNodeSerializer, SystemHostedApplicationSerializer)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ComputerList(APIView):
    def get(self, request, format=None):
        computers = ComputerLapDeskTop.objects.all().order_by('-recorded_date') 
        serializer = ComputerLapDeskTopSerializer(computers, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        serializer = ComputerLapDeskTopSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ComputerDetail(APIView):
    def get_object(self, pk):
        try:
            return ComputerLapDeskTop.objects.get(asset_id=pk) 
        except:
            return None 
    
    def get(self, request, pk, format=None):
        computer = self.get_object(pk)
        if computer:
            serializer = ComputerLapDeskTopSerializer(computer, many=False, context={'request': request})  
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        pass 

    def delete(self, request, pk, format=None):
        pass 

