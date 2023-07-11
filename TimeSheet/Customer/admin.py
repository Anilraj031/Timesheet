from django.contrib import admin
from .models import customer,employee

# Register your models here.
class customerAdmin(admin.ModelAdmin):
    list_display = ('name','address','contact','contract_hr','createdon','status')

admin.site.register(customer,customerAdmin)

class employeesAdmin(admin.ModelAdmin):
    list_display = ('company','email','department')

admin.site.register(employee,employeesAdmin)
