from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import models



def index(request):
    #return HttpResponse("Hello there welcome at the Lenny's django page")
    return render(request,'home.html',{'name':'Lenny'})
def extern(request):
    result = request.POST["num"]
    return render(request,'extern.html',{'result':result})

def test(request):
    return JsonResponse(["Jo dit is mijn API ;)"], safe=False)
    #return "Jo dit is een test"