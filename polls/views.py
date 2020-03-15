from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Device
from .imodel import iDevice
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
    list = []
    print("########################################")
    if request.method == 'GET' and 'id' in request.GET:
        print("Get with id")
    if request.method == "GET":
        print("GET")
        return device_get(request)
        
    if request.method == "POST":
        print("POST")
        return device_post(request)

    if request.method == "PUT":
        print("PUT")
        #return device_delete(request):
        return HttpResponse(status=401)
    
    if request.method == "DELETE":
        print("DELETE")
        #return device_delete(request):
        return HttpResponse(status=404)

# GET
def device_get(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        id = data['id']
        if(id == 0):
            return JsonResponse(["ID 0 does not exist"], safe=False)
        else:
            print("done")
            iDevice.GetDevice(id)
            return JsonResponse(["In progress"], safe=False)
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

# GET
def device_delete(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        id = data['id']
        if(id == 0):
            return JsonResponse(["ID 0 does not exist"], safe=False)
        else:
            print("done")
            iDevice.GetDevice(id)
            return JsonResponse(["In progress"], safe=False)
    except:
        list = iDevice.GetDevices()
        response = json.dumps(list, default=lambda o: o.__dict__, indent=4)
        return HttpResponse(response)    

#/////////////////
# IO

def test(request):
    return JsonResponse(["Succesfull JSON response"], safe=False)
    #return "Jo dit is een test"