from django.shortcuts import render
from .models import customer,employee
# Create your views here.
def index(request):
    all = customer.objects.all()
    return render(request,'customer/customers.html',{'customers':all})

def details(request,id):
    company = customer.objects.get(id=id)
    data = employee.objects.filter(company_id =id )
    return render(request,'customer/customerDetails.html',{'details':data,'company':company})