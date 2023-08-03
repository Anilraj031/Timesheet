from django.shortcuts import render
from .models import customer,employee
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    all = customer.objects.all()
    return render(request,'customer/customers.html',{'customers':all})

@login_required
def details(request,id):
    company = customer.objects.get(id=id)
    data = employee.objects.filter(company_id =id )
    return render(request,'customer/customerDetails.html',{'details':data,'company':company})