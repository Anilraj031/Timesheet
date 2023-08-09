from django.urls import path
from Manager import views

urlpatterns = [
    path('Reports', views.getDetails, name="user_report"),
    path('Users',views.getusers,name="getall"),
    path('CreateUser',views.newUser,name='createUser'),
    path('update/<userId>',views.updateUser,name='updateUser'),
    path('Details/<userId>',views.viewUser,name='userDetails'),
    path('Permission/',views.addPermissions,name="permission"),
    path('LoginType',views.updateLoginType,name="updateLoginType"),
    path('Company/',views.company,name="company"),
    path('Report/',views.report,name='createReport'),
    path('AddMember',views.addManagerMember,name="addtoManager"),
    path('Member',views.removeMember,name="removeMember"),
    path('removeManager',views.removeManager,name="removeManager"),
    path('invoice',views.invoice,name="invoice"),
    path('getInvoice',views.getInvoice,name="getInvoice"),
    path('downloadInvoice/',views.download_invoice_data,name="downloadInvoice"),

    path('send_invite_email/',views.send_invite_email,name='send_invite_email'),
]
