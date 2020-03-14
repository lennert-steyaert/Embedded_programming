from django.core import serializers
import json
from .models import Device
from .models import IO

from .dtos import DTODevice

#################################################################
#///////////////////////////////////////////////////////////////#
#################################################################
#           This file contains the business models
#################################################################
#///////////////////////////////////////////////////////////////#
#################################################################

##################################################
#               Repo for device
##################################################

class iDevice:
    debug = True
    def GetDevices(self):
        # Function variables
        list = []

        # Load query and format to dict
        queryset = Device.objects.all()
        data = serializers.serialize('json', queryset)
        dict = json.loads(data)
        # Loop through dict
        for item in dict:
            pk = item['pk'] # Get primary key
            fields = item['fields'] # Get all fields in sub-dict

            # Get field in record
            name = fields['name']
            lastSync = fields['lastSync']
            lastMessageAccepted = fields['lastMessageAccepted']
            img = fields['img']

            # Put field in device object
            device = Device()
            device.name = name
            device.lastSync = lastSync
            device.lastMessageAccepted = lastMessageAccepted
            device.img = img

            # Put device object DTO object
            dtodevice = DTODevice()
            dtodevice.pk = pk
            dtodevice.IO = []
            dtodevice.device = device
            list.append(dtodevice)

        if self.debug:
            print("###DEBUG###")
            for item in list:
                print(item.pk)
        return list

    def GetDevicesWithIO(self):
        
        return

    def PostDevice(self,deviceDTO):
        return
    
    def PutDevice(self,id,deviceDTO):
        return

    def DeleteDevice(self,id):
        return

    def DeviceCount(self):
        count = Device.objects.all().count()
        print(count)

##################################################
#               Repo for IO
##################################################

class iIO:
    debug = True
    def GetIO(self):
        # Function variables
        list = []

        # Load query and format to dict
        queryset = Device.objects.all()
        data = serializers.serialize('json', queryset)
        dict = json.loads(data)
        # Loop through dict
        for item in dict:
            pk = item['pk'] # Get primary key
            fields = item['fields'] # Get all fields in sub-dict

            # Get field in record
            name = fields['name']
            lastSync = fields['lastSync']
            lastMessageAccepted = fields['lastMessageAccepted']
            img = fields['img']

            # Put field in device object
            device = Device()
            device.name = name
            device.lastSync = lastSync
            device.lastMessageAccepted = lastMessageAccepted
            device.img = img

            # Put device object DTO object
            dtodevice = DTODevice()
            dtodevice.pk = pk
            dtodevice.IO = []
            dtodevice.device = device
            list.append(dtodevice)

        if self.debug:
            print("###DEBUG###")
            for item in list:
                print(item.pk)
        return list

    def PostIO(self,ioDTO):
        return
    
    def PutIO(self,id,ioDTO):
        return

    def PatchIOstateInteger(self,id,integer):
        return

    def PatchIO_stateText(self,id,text):
        return

    def PatchIO_stateDecimal(self,id,decimal):
        return

    def DeleteIO(self,id):
        return