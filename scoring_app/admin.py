from django.contrib import admin
from .models import Person, Calculation, CalculationResult

admin.site.register(Person)
admin.site.register(Calculation)
admin.site.register(CalculationResult)