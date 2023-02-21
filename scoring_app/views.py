from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Something")

def showForm(request, form_id):
    return HttpResponse("Form number %s." % form_id)