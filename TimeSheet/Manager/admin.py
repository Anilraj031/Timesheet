from django.contrib import admin
from Manager.models import InitialPassword,Teams,TeamUsers,TeamLeads

# Register your models here.
class InitialPasswordAdmin(admin.ModelAdmin):
    list_display=('id','user','first_password','first_changed')

class L_Teams(admin.ModelAdmin):
    list_display = ('name','description')

class L_TeamLead(admin.ModelAdmin):
    list_display = ('team','lead')

class L_TeamUser(admin.ModelAdmin):
    list_display = ('team','user')


admin.site.register(InitialPassword,InitialPasswordAdmin)
admin.site.register(Teams,L_Teams)
admin.site.register(TeamLeads,L_TeamLead)
admin.site.register(TeamUsers,L_TeamUser)