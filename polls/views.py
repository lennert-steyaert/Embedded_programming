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
from datetime import timedelta

from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer


from rest_framework.generics import RetrieveAPIView
from .serializers import UserLoginSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import UserProfile

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
    devices = Device.objects.all()
    date = datetime.now()-timedelta(seconds=30)
    return render(request,'home.html',{'devices':devices,'datetime':date})
def extern(request):
    result = request.POST["num"]
    return render(request,'extern.html',{'result':result})
@csrf_exempt
def webios(request):
    data = json.loads(request.body.decode("utf-8"))
    if "pk" in data:
        pk = data["pk"]
    else:
        return HttpResponse(status=404)
    print("DO SCRIPT")
    print(pk)
    ios = iIO.GetDeviceIOs(pk)
    print(ios)
    if(ios == None):
        ios = []
    for io in ios:
        print(io.IO.pin)
    return render(request,'io.html',{'ios':ios})

def webdevices(request):
    devices = Device.objects.all()
    date = datetime.now()-timedelta(seconds=30)
    return render(request,'devices.html',{'devices':devices,'datetime':date})

@csrf_exempt
def webgetio(request):
    if json.loads(request.body.decode("utf-8")) == None:
        return HttpResponse(status=404)
    return io_get(request)

@csrf_exempt
def webputio(request):
    return io_put(request)

#########
# API
#########

#/////////////////
# Device

# SECURE
class DeviceView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        return device_get(request)

    def post(self, request):
        return device_post(request)
    
    def put(self, request):
        return device_put(request)

    def delete(self, request):
        return device_delete(request)

# NOT SECURE
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

# SECURE
class IOView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        return io_get(request)

    def post(self, request):
        return io_post(request)
    
    def put(self, request):
        return io_put(request)

    def delete(self, request):
        return io_delete(request)

# NOT SECURE
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
            ioobj.type = None

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
             ioobj.pin = ""

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
# DeviceIO request

# SECURE
class DeviceIOView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        return deviceio_get(request)


# NOT SECURE
@csrf_exempt
def deviceIO(request):
    print("########################################")
    if request.method == "GET":
        print("GET")
        return deviceio_get(request)

# GET
def deviceio_get(request):
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

#/////////////////
# User

# Secure
class UserRegistrationView(CreateAPIView):

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'User registered  successfully',
            }
        
        return Response(response, status=status_code)
# Secure
class UserLoginView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)
#Secure
class UserProfileView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'first_name': user_profile.first_name,
                    'last_name': user_profile.last_name,
                    'gender': user_profile.gender,
                    }]
                }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)
