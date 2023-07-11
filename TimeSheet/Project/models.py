from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=250,null=False)
    customer = models.CharField(max_length=250)
    estimate_hr = models.DecimalField(null=True,decimal_places=2,max_digits=5)
    worked_hr = models.DecimalField(null=True,decimal_places=2,max_digits=5)
    manager = models.ForeignKey(User,on_delete=models.CASCADE)
    details = models.CharField(max_length=500,null=True)
    created_on = models.DateField(auto_now_add=True)
    estimated_date = models.DateField(null=True)

    def __str__(self):
      return self.name

class SubProject(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    name = models.CharField(max_length=250,null=False)
    details = models.CharField(max_length=500,null=True)
    assigned_to = models.ForeignKey(User,on_delete=models.CASCADE)
    hour = models.DecimalField(null=True,decimal_places=2,max_digits=5)
    hours_done = models.DecimalField(null=True,decimal_places=2,max_digits=5,default=None)

    def __str__(self):
      return self.name