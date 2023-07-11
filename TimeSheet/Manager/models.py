from django.db import models
from django.contrib.auth.models import User
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


