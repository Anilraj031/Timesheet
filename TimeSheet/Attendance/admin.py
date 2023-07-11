from django.contrib import admin
from Attendance.models import Attendance, Leave, LeaveType, Approval, TrackAttendance

# Register your models here.
class AttendanceAdmin(admin.ModelAdmin):
  list_display = ('id','date','day','user','entry','lbreak1','lbreak2','exit','hour','start_location','stop_location')

class LeaveTyepAdmin(admin.ModelAdmin):
  list_display = ('id','name','days')

class ApprovalAdmin(admin.ModelAdmin):
  list_display = ('id','name')

class LeaveAdmin(admin.ModelAdmin):
  list_display = ('date','user','type','leave_from','leave_to','details','approval','approved_by','date_approved')

class TrackAdmin(admin.ModelAdmin):
  list_display = ('user','btn1','btn2','btn3')

admin.site.register(TrackAttendance,TrackAdmin)
admin.site.register(LeaveType,LeaveTyepAdmin)
admin.site.register(Leave,LeaveAdmin)
admin.site.register(Approval,ApprovalAdmin)
admin.site.register(Attendance,AttendanceAdmin)