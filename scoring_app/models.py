from django.db import models

class Person(models.Model):
    nick_name = models.CharField(max_length=30)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)