"""TimeSheet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from TimeSheet import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="home"),
    path('login', views.login, name='login2'),
    path('activity',views.myActivity,name='getmyactivity'),
    path('test', views.test, name='test'),
    path('validate/', include('Authentication.urls')),
    path('Attendance/', include('Attendance.urls')),
    path('Manage/',include('Manager.urls')),
    path('Project/',include('Project.urls')),
    path('Worklog/',include('emp_worklog.urls')),
    path('Issue/',include('Issue.urls')),
    path('Customer/',include('Customer.urls'))
    
    
]
