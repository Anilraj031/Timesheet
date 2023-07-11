from django.db import models

# Create your models here.
class customer(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    contact = models.EmailField(max_length=50)
    contract_hr = models.IntegerField(null=True)
    createdon=models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50)

class employee(models.Model):
    company = models.ForeignKey(customer,null=True,on_delete=models.SET_NULL)
    email = models.EmailField(max_length=254)
    department = models.CharField(max_length=50,null=True)
