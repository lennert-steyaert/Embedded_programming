from django.core import serializers
import json
from .models import Device
from .models import IO
from .models import Type

from .dtos import DTODevice
from .dtos import DTOIO

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

    def DictToList(self,dict):
        # Function variables
        list = []

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
        return list

    def GetDevices(self):
        # Get objects from DB
        queryset = Device.objects.all()
        # Queryset to JSON
        data = serializers.serialize('json', queryset)
        # Load JSON as dictionary
        dict = json.loads(data)
        # Put data in list
        result = self.DictToList(dict)
        # Debug
        if self.debug:
            print("###DEBUG###")
            for item in result:
                print(item.pk)

        return result

    def GetDevice(self,id):
        # Get object from DB
        queryset = Device.objects.filter(pk=id)
        if(not queryset):
            return None
        else:
            # Queryset to JSON
            data = serializers.serialize('json', queryset)
            # Load JSON as dictionary
            dict = json.loads(data)
            # Put data in list
            result = self.DictToList(dict)
            return result

    def GetDeviceByName(self,name):
        return

    def PostDevice(self,device):
        # Save device in DB
        device.save()
        # Get object from DB
        queryset = Device.objects.filter(pk=device.pk)
        # Queryset to JSON
        data = serializers.serialize('json', queryset)
        # Load JSON as dictionary
        dict = json.loads(data)
        # Put data in list
        result = self.DictToList(dict)
        
        return result
    
    def PutDevice(self,id,deviceDTO):
        queryfind = Device.objects.filter(pk=id)
        if(not queryfind):
            return None
        else:
            queryset = Device.objects.get(pk=id)
            queryset.name = deviceDTO.name
            queryset.lastSync = deviceDTO.lastSync
            queryset.lastSync = deviceDTO.lastSync
            queryset.lastMessageAccepted = deviceDTO.lastMessageAccepted
            queryset.img = deviceDTO.img

            queryset.save()

            # Get object from DB
            queryset = Device.objects.filter(pk=id)
            # Queryset to JSON
            data = serializers.serialize('json', queryset)
            # Load JSON as dictionary
            dict = json.loads(data)
            # Put data in list
            result = self.DictToList(dict)
            return result

    def DeleteDevice(self,id):
        # Get object from DB
        queryset = Device.objects.filter(pk=id)
        if(not queryset):
            return False
        else:
            # Delete record
            queryset.delete()
            return True
        return

    def DeviceCount(self):
        count = Device.objects.all().count()
        print(count)



##################################################
#               Repo for IO
##################################################

class iIO:
    debug = True
    def DictToList(self,dict):
        # Function variables
        list = []

        # Loop through dict
        for item in dict:
            pk = item['pk'] # Get primary key
            fields = item['fields'] # Get all fields in sub-dict

            # Get field in record
            type = fields['type']
            stateInteger = fields['stateInteger']
            stateText = fields['stateText']
            stateDecimal = fields['stateDecimal']
            device = fields['device']
            pin = fields['pin']

            # Put field in IO object
            io = IO()
            io.type = type
            io.stateInteger = stateInteger
            io.stateText = stateText
            io.stateDecimal = stateDecimal
            io.pin = pin
            #io.device = device

            # Put IO object DTO object
            dtoio = DTOIO()
            dtoio.pk = pk
            dtoio.device = device
            dtoio.IO = io
            
            list.append(dtoio)
        return list

    def GetIOs(self):
        # Get object from DB
        queryset = IO.objects.all()
        if(not queryset):
            return None
        else:
            # Queryset to JSON
            data = serializers.serialize('json', queryset)
            # Load JSON as dictionary
            dict = json.loads(data)
            # Put data in list
            result = self.DictToList(dict)
            return result

    def GetIO(self,id):
        # Get object from DB
        queryset = IO.objects.filter(pk=id)
        if(not queryset):
            return None
        else:
            # Queryset to JSON
            data = serializers.serialize('json', queryset)
            # Load JSON as dictionary
            dict = json.loads(data)
            # Put data in list
            result = self.DictToList(dict)
            return result

    def PostIO(self,ioDTO,deviceId):
        try:
            queryDevice = Device.objects.get(pk=deviceId)
        except:
            return None

        ioDTO.device = queryDevice
        # Save device in DB
        ioDTO.save()
        # Get object from DB
        queryset = IO.objects.filter(pk=ioDTO.pk)
        # Queryset to JSON
        data = serializers.serialize('json', queryset)
        # Load JSON as dictionary
        dict = json.loads(data)
        # Put data in list
        result = self.DictToList(dict)
        
        return result
    
    def PutIO(self,id,ioDTO):
        queryfind = IO.objects.filter(pk=id)
        if(not queryfind):
            return None
        else:
            queryset = IO.objects.get(pk=id)
            queryset.type = ioDTO.type
            queryset.stateInteger = ioDTO.stateInteger
            queryset.stateText = ioDTO.stateText
            queryset.stateDecimal = ioDTO.stateDecimal
            queryset.pin = ioDTO.pin

            queryset.save()

            # Get object from DB
            queryset = IO.objects.filter(pk=id)
            # Queryset to JSON
            data = serializers.serialize('json', queryset)
            # Load JSON as dictionary
            dict = json.loads(data)
            # Put data in list
            result = self.DictToList(dict)
            return result
        return

    def PatchIOstateInteger(self,id,integer):
        return

    def PatchIO_stateText(self,id,text):
        return

    def PatchIO_stateDecimal(self,id,decimal):
        return

    def DeleteIO(self,id):
        # Get object from DB
        queryset = IO.objects.filter(pk=id)
        if(not queryset):
            return False
        else:
            # Delete record
            queryset.delete()
            return True
    
    def GetDeviceIOs(self,id):
        queryset = IO.objects.filter(device=id)
        print(queryset)
        if(not queryset):
            return None
        else:
            # Queryset to JSON
            data = serializers.serialize('json', queryset)
            # Load JSON as dictionary
            dict = json.loads(data)
            # Put data in list
            result = self.DictToList(dict)
            return result