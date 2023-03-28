from django.db import models


import django
# Create your models here.

class UserInfo(models.Medel):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
