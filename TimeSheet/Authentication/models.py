from django.db import models
from django.contrib.auth.models import User,AbstractUser

# Create your models here.
class userDetails(models.Model):
    user = models.ForeignKey(User, null=True, on_delete= models.SET_NULL)
    attendanceType = models.CharField(max_length=100,null=True,default="Physical")
    mrequest = models.BooleanField("Request", default=False, null=True)
    is_manager = models.BooleanField("Manager", default=False, null=True)

    def __str__(self):
      return self.user.username

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
    device = models.CharField( max_length=200,default='before')

class Role(models.Model):
    name = models.CharField( max_length=200,default='User')

class userRoles(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    role = models.ForeignKey(Role,on_delete=models.SET_NULL,null=True)


class userManager(models.Model):
    manager = models.ForeignKey(userDetails,on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)



