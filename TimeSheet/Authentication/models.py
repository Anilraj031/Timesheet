from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class userDetails(models.Model):
    user = models.ForeignKey(User, null=True, on_delete= models.SET_NULL)
    attendanceType = models.CharField(max_length=100,null=True,default="Physical")
    mrequest = models.BooleanField("Request", default=False, null=True)

class Company(models.Model):
    user = models.ForeignKey(User, null=True, on_delete= models.SET_NULL)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone1 = models.CharField( max_length=50)
    phone2 = models.CharField( max_length=50)
    email = models.EmailField()
    contact_email =models.EmailField()

    def __str__(self):
      return self.name


class Employees(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class LoggedUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

