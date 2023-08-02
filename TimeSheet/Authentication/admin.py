from django.contrib import admin
from Authentication.models import LoggedUser,Company,Employees,userDetails,userManager

# Register your models here.
#@admin.site.register(LoggedUser)
class LoggedAdmin(admin.ModelAdmin):
    list_display=('id','user','device')

class compAdmin(admin.ModelAdmin):
    list_display=('user','name','address','phone1','phone2','email','contact_email')

class userCompAdmin(admin.ModelAdmin):
    list_display = ('company','user')

class uDetails(admin.ModelAdmin):
    list_display = ('user','attendanceType','mrequest','is_manager','is_mfa')

class uManager(admin.ModelAdmin):
    list_display = ('manager','user')

admin.site.register(userManager,uManager)
admin.site.register(userDetails,uDetails)
admin.site.register(Employees,userCompAdmin)
admin.site.register(LoggedUser,LoggedAdmin)
admin.site.register(Company,compAdmin)