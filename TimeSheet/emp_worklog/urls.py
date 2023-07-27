from django.urls import path
from . import views 
urlpatterns = [
    path('', views.index),
    path('index/', views.index),
    path('dailylog1/', views.dailylog1),
    path('billable/', views.billable),
    path('nonbillable/', views.nonbillable),
    path('loginpage/', views.loginpage),
    path('test/', views.test),
    path('enterrecord/', views.enterrecord),
    path('addrecord/', views.addrecord),
    path('dailylog/', views.dailylog, name='dailylog'),
    path('add', views.ADD, name='addLog'),

    path('edit', views.Edit, name='getLog'),
    path('update/<str:id>', views.Update, name='update'),
    path('delete/<str:id>', views.Delete, name='delete'),
    path('project',views.gets, name='project'),
    path('subproject',views.subproject, name='subproject'),
    path('gethours',views.getMonthlyHours,name='getMonthlyHours'),
    path('hours',views.getHoursData,name="getHours"),
    path('usersLog',views.usersLog,name="usersLog"),
    path('getUserLog',views.getLogByUsers,name="getlogbyuser"),
    path('downloadLog',views.download_excel_data,name="downloadLog")
    # path('filter/', views.filter)
]
 