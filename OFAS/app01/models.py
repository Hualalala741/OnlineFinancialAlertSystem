from django.db import models

# Create your models here.
class UserInfo11(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    city = models.CharField(max_length=32)

