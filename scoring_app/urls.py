from django.urls import path
from . import views
from .forms import SignInForm

urlpatterns = [
    path('home/', views.home, name='home'),
    path('form/', views.form, name='form'),
    path('contact/', views.contact, name='contact'),
    path('result/', views.calculation_result, name='result'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('sign-in/', views.sign_in, name='sign-in'),
    path('sign-out/', views.sign_out, name='sign-out'),
]