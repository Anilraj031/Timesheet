from django.contrib import admin
from Dashboard.models import Employee, Attendance
# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name','username','email','password','company')

class AttendanceAdmin(admin.ModelAdmin):
  list_display = ('id','date','day','user','entry','lbreak1','lbreak2','exit','hour','start_location','stop_location')

admin.site.register(Attendance,AttendanceAdmin)
admin.site.register(Employee,EmployeeAdmin)