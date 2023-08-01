from django.contrib import admin
from .models import worklog, tasktype, LogApproval
# Register your models here.
class display(admin.ModelAdmin):
    list_display=['id','User', 'Date', 'TaskType', 'project_id','task','Workdone', 'Hours', 'Billable',] 

class taskAdmin(admin.ModelAdmin):
    list_display = ('id','TaskType')

admin.site.register(LogApproval)
admin.site.register(tasktype,taskAdmin)
admin.site.register(worklog,display)





