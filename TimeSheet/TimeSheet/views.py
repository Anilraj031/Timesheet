from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from Dashboard.models import Employee,Attendance
from django.views.decorators.csrf import csrf_exempt
import datetime
from geopy.geocoders import Nominatim
from django.urls import reverse
from Authentication.models import LoggedUser
from Attendance.models import Leave,Attendance
from django.contrib.auth.models import User
from Manager.views import checkTeams
from Issue.models import Ticket
from django.db.models import Q
from django.db.models import Sum
from emp_worklog.models import worklog

def index(request):
	if request.user.is_authenticated :
		#is_manager = checkTeams(request)
		issues = Ticket.objects.filter(Q(state='InProgress'))
		worklogs =worklog.objects.filter(Date__month=datetime.date.today().month)
		check_users=checkTeams(request)
		users=User.objects.filter(Q(pk__in=check_users[0]) | Q(id=request.user.id))
		usr_hour = []
		for x in users:
			usr_hour.append({
				'user':x,
				'billable':worklog.objects.filter(Date__month=datetime.date.today().month,User = x.id,Billable=True).aggregate(Sum('Hours')).get('Hours__sum', 0.00),
				'nonbillable':worklog.objects.filter(Date__month=datetime.date.today().month,User = x.id,Billable=False).aggregate(Sum('Hours')).get('Hours__sum', 0.00)
			})
		print(usr_hour)
		if request.user.is_superuser:
			atdnc = Attendance.objects.filter(date=datetime.date.today())
			activeUser = LoggedUser.objects.all().count()
			totalUser = User.objects.all().count()
			onLeave = Leave.objects.filter(date=datetime.date.today(),approval=1).count()
			pendingApproval = Leave.objects.filter(date=datetime.date.today(),approval=2).count()
			return render(request, 'index.html',{'active':activeUser,'total':totalUser,'onleave':onLeave,'pending':pendingApproval,'todaysAtten':atdnc,'issue':issues,'wlogs':worklogs,'hours':usr_hour})
		else:
			user = checkTeams(request)
			atdnc = Attendance.objects.filter(Q(user__in=user[0])|Q(user=request.user),date=datetime.date.today())
			return render(request, 'index.html',{'todaysAtten':atdnc,'issue':issues,'wlogs':worklogs,'hours':usr_hour})
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