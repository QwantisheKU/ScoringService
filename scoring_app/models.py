from datetime import datetime
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=30, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

class Calculation(models.Model):
    LOAN_DEFAULTS = (
        ('Y', 'Да'),
        ('N', 'Нет'),
    )
    HOME_OWNERSHIPS = (
        ('RENT', 'Аренда'),
        ('MORTGAGE', 'Ипотека'),
        ('OWN', 'Собственность'),
        ('OTHER', 'Другое'),
    )
    LOAN_INTENTS = (
        ('EDUCATION', 'Образование'),
        ('MEDICAL', 'Медицина'),
        ('VENTURE', 'Инвестиции'),
        ('PERSONAL', 'Личная'),
        ('DEBTCONSOLIDATION', 'Погашение долга'),
        ('HOMEIMPROVEMENT', 'Жилищный ремонт'),
    )
    person_name = models.CharField(max_length=200)
    person_age = models.IntegerField()
    person_income = models.IntegerField()
    person_home_ownership = models.CharField(max_length=30, choices=HOME_OWNERSHIPS)
    person_emp_length = models.FloatField()
    loan_intent = models.CharField(max_length=30, choices=LOAN_INTENTS)
    loan_amnt = models.IntegerField()
    loan_int_rate = models.FloatField()
    cb_person_default_on_file = models.CharField(max_length=30, choices=LOAN_DEFAULTS)
    cb_person_cred_hist_length = models.IntegerField()
    date_created = models.DateTimeField(default=datetime.now)
    person_id = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.person_name
    
class CalculationResult(models.Model):
    score = models.CharField(max_length=1)
    date_created = models.DateTimeField(default=datetime.now)
    calculation_id = models.ForeignKey(Calculation, null=True, on_delete=models.SET_NULL)
    