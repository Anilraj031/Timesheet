from django.contrib import admin
from .models import worklog, tasktype
# Register your models here.
class display(admin.ModelAdmin):
    list_display=['id','User', 'Date', 'TaskType', 'project_id','task','Workdone', 'Hours', 'Billable',] 

class taskAdmin(admin.ModelAdmin):
    list_display = ('id','TaskType')
# admin.site.register(display)
admin.site.register(tasktype,taskAdmin)
admin.site.register(worklog,display)





