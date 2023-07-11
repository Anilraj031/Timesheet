from django.urls import path

from Project import views

urlpatterns = [
    path('all',views.projects,name='aproject'),
    path('details/<pid>',views.getProject,name='projectDetails'),
    path('subtasks/',views.getSubDetails,name='subTaskDetails'),
    
]