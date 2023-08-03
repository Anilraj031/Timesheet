from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class InitialPassword(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    first_password = models.CharField(null=True,max_length=50)
    first_changed = models.BooleanField(null=True)

class Teams(models.Model):
    name = models.CharField(null=True,max_length=100)
    description = models.CharField(null=True,max_length=300)

    def __str__(self):
      return self.name

class TeamLeads(models.Model):
    team = models.ForeignKey(Teams, null=True, on_delete=models.SET_NULL)
    lead = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

class TeamUsers(models.Model):
    team = models.ForeignKey(Teams, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


class FilterQuery(models.Model):
    type = models.CharField(null=True,max_length=100)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    date1 = models.DateField(default=timezone.now)
    date2 = models.DateField(default=timezone.now)
    task_type = models.CharField(null=True,max_length=100)
    log_type = models.CharField(null=True,max_length=100)

class Notifications(models.Model):
    table = models.CharField(null=True,max_length=100)
    row = models.IntegerField(null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    
    details = models.BooleanField(default=False, null=True)
    alert_status = models.BooleanField(default=False, null=True)
    seen_status = models.BooleanField(default=False, null=True)
    

