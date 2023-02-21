from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('form/<int:form_id>/', views.showForm, name='showForm')
]