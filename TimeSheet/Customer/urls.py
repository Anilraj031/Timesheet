from django.urls import path
from Customer import views

urlpatterns = [
    path('', views.index, name="allcustomers"),
    path('details/<id>',views.details, name="customerDetails"),
    
]