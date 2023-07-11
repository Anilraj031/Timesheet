from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Attendance(models.Model):
    date = models.DateField(auto_now_add=True,null=True)
    day = models.CharField(max_length=50,null=True)
    user = models.ForeignKey(User, null=True, on_delete= models.SET_NULL)
    entry = models.CharField(max_length=50)
    lbreak1 = models.CharField(max_length=50,null=True)
    lbreak2 = models.CharField(max_length=50,null=True)
    exit = models.CharField(max_length=50, null=True)
    hour = models.CharField(max_length=50, null=True)
    type = models.CharField(max_length=50,null=True,default=None)
    start_location = models.CharField(max_length=500, null=True)
    stop_location = models.CharField(max_length=500, null=True)

class LeaveType(models.Model):
    name = models.CharField(max_length=50,null=True,default=None)
    days = models.IntegerField(null=True,)

    def __str__(self):
      return self.name

class Approval(models.Model):
    name =models.CharField(max_length=50)
    def __str__(self):
      return self.name

class Leave(models.Model):
    date =  models.DateField(auto_now_add=True,null=True)
    user = models.ForeignKey(User, null=True, on_delete= models.SET_NULL)
    type =  models.ForeignKey(LeaveType,on_delete= models.CASCADE)
    leave_from = models.DateField(null=True)
    leave_to = models.DateField(null=True)
    details = models.TextField()
    approval = models.ForeignKey(Approval, on_delete=models.CASCADE, null=True,default=2)
    approved_by = models.CharField(max_length=50,null=True)
    date_approved = models.DateTimeField(null=True,default=None)

class TrackAttendance(models.Model):
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    btn1 = models.BooleanField(null=True)
    btn2 = models.BooleanField(null=True)
    btn3 = models.BooleanField(null=True)


