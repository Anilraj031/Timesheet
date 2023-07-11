from django.db import models

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password =models.CharField(max_length=50)
    company = models.CharField(max_length=50, default='Glacier', null=True)

class Attendance(models.Model):
    date = models.DateField(auto_now_add=True,null=True)
    day = models.CharField(max_length=50,null=True)
    user = models.CharField(max_length=50,null=True)
    entry = models.CharField(max_length=50)
    lbreak1 = models.CharField(max_length=50,null=True)
    lbreak2 = models.CharField(max_length=50,null=True)
    exit = models.CharField(max_length=50, null=True)
    hour = models.CharField(max_length=50, null=True)
    start_location = models.CharField(max_length=500, null=True)
    stop_location = models.CharField(max_length=500, null=True)