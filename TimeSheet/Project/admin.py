from django.contrib import admin
from Project.models import Project,SubProject
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name','customer','estimate_hr','worked_hr','manager','details','created_on','estimated_date')

class SubAdmin(admin.ModelAdmin):
    list_display = ('project','name','details','assigned_to','hour','hours_done')

admin.site.register(Project,ProjectAdmin)
admin.site.register(SubProject,SubAdmin)