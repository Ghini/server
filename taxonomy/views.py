from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    response = "My List of Employees Goes Here"
    return HttpResponse(response)
