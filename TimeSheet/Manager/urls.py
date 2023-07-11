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
]
