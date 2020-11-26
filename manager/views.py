from django.http import HttpResponse
from django.shortcuts import render

def hello(requests):
    return HttpResponse("Hello world")

def buybook(requests):
    return HttpResponse("Black Friday!!!")


# Create your views here.
