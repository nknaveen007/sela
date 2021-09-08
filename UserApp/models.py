from django.db import models
from django.db.models.fields import CharField

# Create your models here.

class UserData(models.Model):
    UserId = models.AutoField(primary_key=True)
    UserStatus =models.IntegerField(default=1)
    PhoneNumber = models.CharField(max_length=12,default='')
    Name=models.CharField(max_length=100,default='')
    SelaId=models.CharField(max_length=50,default='')
