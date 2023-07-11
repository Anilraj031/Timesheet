from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from Dashboard.models import Employee,Attendance
from django.views.decorators.csrf import csrf_exempt
import datetime
from geopy.geocoders import Nominatim
from django.urls import reverse
from Authentication.models import LoggedUser
from Attendance.models import Leave
from django.contrib.auth.models import User

def index(request):
	if request.user.is_authenticated :
		if request.user.is_superuser:
			activeUser = LoggedUser.objects.all().count()
			totalUser = User.objects.all().count()
			onLeave = Leave.objects.filter(date=datetime.date.today(),approval=1).count()
			pendingApproval = Leave.objects.filter(date=datetime.date.today(),approval=2).count()
			return render(request, 'index.html',{'active':activeUser,'total':totalUser,'onleave':onLeave,'pending':pendingApproval})
		else:
			return render(request, 'index.html')
	else:
		return HttpResponseRedirect(reverse('login'))

def login(request):
	return render(request, 'login.html')

def test(request):
	geolocator = Nominatim(user_agent="geoapiExercises")
	#Latitude = "25.594095"
	#Longitude = "85.137566"
	
	#lazimpat
	Latitude = "27.723466120043092"
	Longitude = "85.32408337457957"

	#Mhepi
	#Latitude = "27.726346"
	#Longitude = '85.308847'
	
	location = geolocator.reverse(Latitude+","+Longitude)
	
	address = location.raw['address']
	city = address.get('city', '')
	street = address.get('street_name','')
	state = address.get('state', '')
	country = address.get('country', '')
	code = address.get('country_code')
	zipcode = address.get('postcode')
	return HttpResponse(location)