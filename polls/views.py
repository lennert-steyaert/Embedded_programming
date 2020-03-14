from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .imodel import iDevice
import json
from django.core import serializers

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

@csrf_exempt
def device(request):
    list = []
    print("########################################")
    if request.method == 'GET' and 'id' in request.GET:
        print("Get with id")
    if request.method == "GET":
        print("GET")
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
        
    if request.method == "POST":
        print("POST")

            
    response = json.dumps(list, default=lambda o: o.__dict__, indent=4)
    return HttpResponse(response)

def test(request):
    return JsonResponse(["Succesfull JSON response"], safe=False)
    #return "Jo dit is een test"