from django.db import models

class User(models.Model):
    nick_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

class Form(models.Model):
    person_name = models.CharField(max_length=200)
    person_age = models.IntegerField()
    person_income = models.IntegerField()
    person_home_ownership = models.CharField(max_length=30)
    person_emp_length = models.FloatField()
    loan_intent = models.CharField(max_length=30)
    loan_amnt = models.IntegerField()
    loan_int_rate = models.FloatField()
    loan_percent_income = models.FloatField()
    cb_person_default_on_file = models.FloatField()
    cb_person_cred_hist_length = models.IntegerField()
    person_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.person_id
