from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'scoring_app/home.html')

def form(request):
    return render(request, 'scoring_app/form.html')

def contact(request):
    return render(request, 'scoring_app/contact.html')