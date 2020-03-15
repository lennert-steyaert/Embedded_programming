from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Device
from .models import IO
from .imodel import iDevice
from .imodel import iIO
import json
from django.core import serializers
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt

#################################################################
#///////////////////////////////////////////////////////////////#
#################################################################
# This file contains the view in python (controllers)
#################################################################
#///////////////////////////////////////////////////////////////#
#################################################################


##################################################
#               Global variables
##################################################

iDevice = iDevice()
iIO = iIO()

##################################################
#                  Controllers
##################################################

#########
# Media
#########

def index(request):
    #return HttpResponse("Hello there welcome at the Lenny's django page")
    return render(request,'home.html',{'name':'Lenny'})
def extern(request):
    result = request.POST["num"]
    return render(request,'extern.html',{'result':result})

#########
# API
#########

#/////////////////
# Device
@csrf_exempt
def device(request):
    print("########################################")
    if request.method == "GET":
        print("GET")
        return device_get(request)
        
    if request.method == "POST":
        print("POST")
        return device_post(request)

    if request.method == "PUT":
        print("PUT")
        return device_put(request)
    
    if request.method == "DELETE":
        print("DELETE")
        return device_delete(request)

# GET
def device_get(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        print(type(data)) 
        print(data)
        id = data['id']
        if(id == 0):
            return HttpResponse(status=404)
        else:
            dtodevice = iDevice.GetDevice(id)
            if(dtodevice == None):
                return HttpResponse(status=404)
            response = json.dumps(dtodevice, default=lambda o: o.__dict__, indent=4)
            return HttpResponse(response)
    except:
        list = iDevice.GetDevices()
        response = json.dumps(list, default=lambda o: o.__dict__, indent=4)
        return HttpResponse(response)    

# POST
def device_post(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        print(type(data)) 
        print(data)
        if "device" in data:
            device = data["device"]
        else:
            return HttpResponse(status=409)
        deviceobj = Device()
        if "name" in device:
            deviceobj.name = device["name"]
        else:
            return HttpResponse(status=409)
        if "lastSync" in device:
            deviceobj.lastSync = device["lastSync"]
        else:
            #return HttpResponse(status=409)  
            deviceobj.lastSync = datetime.now()
        if "lastMessageAccepted" in device:
            deviceobj.lastMessageAccepted =  device["lastMessageAccepted"]
        else:
            #return HttpResponse(status=409) 
            deviceobj.lastMessageAccepted = True

        deviceobj.img = device["img"]

        dtodevice = iDevice.PostDevice(deviceobj)
        response = json.dumps(dtodevice, default=lambda o: o.__dict__, indent=4)
        return HttpResponse(response)
        #return HttpResponse(status=201)
        #return JsonResponse(["Succesfull JSON response"], safe=False)
    except:
        return HttpResponse(status=500)

# PUT
def device_put(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        print(type(data)) 
        print(data)
        if "pk" in data:
            id = data["pk"]
        else:
            return HttpResponse(status=409)  
        if "device" in data:
            device = data["device"]
        else:
            return HttpResponse(status=409)
        deviceobj = Device()
        if "name" in device:
            deviceobj.name = device["name"]
        else:
            return HttpResponse(status=409)
        if "lastSync" in device:
            deviceobj.lastSync = device["lastSync"]
        else:
            deviceobj.lastSync = datetime.now()
        if "lastMessageAccepted" in device:
            deviceobj.lastMessageAccepted =  device["lastMessageAccepted"]
        else:
            deviceobj.lastMessageAccepted = True

        deviceobj.img = device["img"]

        dtodevice = iDevice.PutDevice(id,deviceobj)
        if(dtodevice == None):
            print("error")
            return HttpResponse(status=404)
        response = json.dumps(dtodevice, default=lambda o: o.__dict__, indent=4)
        return HttpResponse(response)
    except:
        return HttpResponse(status=500)

# DELETE
def device_delete(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        print(type(data)) 
        print(data)
        id = data['id']
        if(id == 0):
            return HttpResponse(status=404)
        else:
            if(iDevice.DeleteDevice(id)):
                return HttpResponse(status=204)
            else:
                return HttpResponse(status=404)
    except:
        return HttpResponse(status=404)

#/////////////////
# IO

@csrf_exempt
def io(request):
    print("########################################")
    if request.method == "GET":
        print("GET")
        return io_get(request)
        
    if request.method == "POST":
        print("POST")
        return io_post(request)

    if request.method == "PUT":
        print("PUT")
        return io_put(request)
    
    if request.method == "DELETE":
        print("DELETE")
        return io_delete(request)

# GET
def io_get(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        print(type(data)) 
        print(data)
        id = data['id']
        if(id == 0):
            return HttpResponse(status=404)
        else:
            dtoio = iIO.GetIO(id)
            if(dtoio == None):
                return HttpResponse(status=404)
            response = json.dumps(dtoio, default=lambda o: o.__dict__, indent=4)
            return HttpResponse(response)
    except:
        list = iIO.GetIOs()
        response = json.dumps(list, default=lambda o: o.__dict__, indent=4)
        return HttpResponse(response)    

# POST
def io_post(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        print(type(data)) 
        print(data)
        if "device" in data:
            deviceId = data["device"]
        else:
            return HttpResponse(status=409)

        if "IO" in data:
            io = data["IO"]
        else:
            return HttpResponse(status=409)

        ioobj = IO()
        if "type" in io:
            ioobj.type = io["type"]
        else:
            return HttpResponse(status=409)

        if "stateInteger" in io:
            ioobj.stateInteger = io["stateInteger"]
        else:
            ioobj.stateInteger = 0

        if "stateText" in io:
            ioobj.stateText = io["stateText"]
        else:
            ioobj.stateText = ""
        
        if "stateDecimal" in io:
            ioobj.stateDecimal = io["stateDecimal"]
        else:
            ioobj.stateDecimal = 0.0
        if "pin" in io:
            ioobj.pin = io["pin"]
        else:
             ioobj.pin = "EMPTY"

        dtoio = iIO.PostIO(ioobj,deviceId)
        if(dtoio == None):
            return HttpResponse(status=409)
        response = json.dumps(dtoio, default=lambda o: o.__dict__, indent=4)
        return HttpResponse(response)
    except:
        return HttpResponse(status=500)

# PUT
def io_put(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        print(type(data)) 
        print(data)
        if "pk" in data:
            id = data["pk"]
        else:
            return HttpResponse(status=409)  
        if "device" in data:
            deviceId = data["device"]
        else:
            return HttpResponse(status=409)

        if "IO" in data:
            io = data["IO"]
        else:
            return HttpResponse(status=409)

        ioobj = IO()
        if "type" in io:
            ioobj.type = io["type"]
        else:
            return HttpResponse(status=409)

        if "stateInteger" in io:
            ioobj.stateInteger = io["stateInteger"]
        else:
            ioobj.stateInteger = 0

        if "stateText" in io:
            ioobj.stateText = io["stateText"]
        else:
            ioobj.stateText = ""
        
        if "stateDecimal" in io:
            ioobj.stateDecimal = io["stateDecimal"]
        else:
            ioobj.stateDecimal = 0.0
        
        if "pin" in io:
            ioobj.pin = io["pin"]
        else:
             ioobj.pin = "EMPTY"

        dtoio = iIO.PutIO(id,ioobj)

        if(dtoio == None):
            print("error")
            return HttpResponse(status=404)
        response = json.dumps(dtoio, default=lambda o: o.__dict__, indent=4)
        return HttpResponse(response)
    except:
        return HttpResponse(status=500)

# DELETE
def io_delete(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        print(type(data)) 
        print(data)
        id = data['id']
        if(id == 0):
            return HttpResponse(status=404)
        else:
            if(iIO.DeleteIO(id)):
                return HttpResponse(status=204)
            else:
                return HttpResponse(status=409)
    except:
        return HttpResponse(status=404)

#/////////////////
# IO

@csrf_exempt
def deviceIO(request):
    print("########################################")
    if request.method == "GET":
        print("GET")
        return deviceIO_get(request)

# GET
def deviceIO_get(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        print(type(data)) 
        print(data)
        id = data['id']
        if(id == 0):
            return HttpResponse(status=404)
        else:
            list = iIO.GetDeviceIOs(id)
            if(list == None):
                return HttpResponse(status=404)
            response = json.dumps(list, default=lambda o: o.__dict__, indent=4)
            return HttpResponse(response)
    except:
        return HttpResponse(status=404)    