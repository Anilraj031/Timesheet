from django.contrib import admin
from .models import Ticket,ticketDetails
# Register your models here.
class display(admin.ModelAdmin):
    list_display = ('id','ticket_name','ticket_type','company')
admin.site.register(Ticket,display)

class displayDetails(admin.ModelAdmin):
    list_display = ('ticket','comments','date','user')

admin.site.register(ticketDetails,displayDetails)
