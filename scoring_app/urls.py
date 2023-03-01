from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('form/', views.form, name='form'),
    path('contact/', views.contact, name='contact'),
    path('result/', views.calculation_result, name='result'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('sign-in/', views.sign_in, name='sign_in'),
]