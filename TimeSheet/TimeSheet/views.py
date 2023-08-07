from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from Dashboard.models import Employee,Attendance
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from django.urls import reverse
from Authentication.models import LoggedUser
from Attendance.models import Leave,Attendance
from django.contrib.auth.models import User
from Manager.views import checkTeams
from Issue.models import Ticket
from django.db.models import Q
from django.db.models import Sum
from emp_worklog.models import worklog,LogApproval

def index(request):
	if request.user.is_authenticated :
		is_manager = checkTeams(request)
		issues = Ticket.objects.filter(Q(state='InProgress')|Q(state='New'))
		worklogs =worklog.objects.filter(Date__month=datetime.now().today().month)
		check_users=checkTeams(request)
		users=User.objects.filter(Q(pk__in=check_users[0]) | Q(id=request.user.id))
		usr_hour = []
		for x in users:
			usr_hour.append({
				'user':x,
				'billable':worklog.objects.filter(Date__month=datetime.now().today().month,User = x.id,Billable=True).aggregate(Sum('Hours')).get('Hours__sum', 0.00),
				'nonbillable':worklog.objects.filter(Date__month=datetime.now().today().month,User = x.id,Billable=False).aggregate(Sum('Hours')).get('Hours__sum', 0.00)
			})
		#print(usr_hour)
		if is_manager[1] == True :
			atdnc = Attendance.objects.filter(date=datetime.now().today())
			activeUser = LoggedUser.objects.filter(Q(pk__in=is_manager[0])|Q(user=request.user)).count()
			totalUser = User.objects.filter(pk__in=is_manager[0]).count()
			onLeave = Leave.objects.filter(date=datetime.now().today(),approval=1).count()
			pendingApproval = Leave.objects.filter(date=datetime.now().today(),approval=2).count()
			return render(request, 'index.html',{'active':activeUser,'total':totalUser,'onleave':onLeave,'pending':pendingApproval,'todaysAtten':atdnc,'issue':issues,'wlogs':worklogs,'hours':usr_hour})
		else:
			user = checkTeams(request)
			atdnc = Attendance.objects.filter(Q(user__in=user[0])|Q(user=request.user),date=datetime.now().today())
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



def myActivity(request):
	days = int(request.GET['days'])

	t_month = datetime.now().today().month
	log_approval = LogApproval.objects.filter(user=request.user,month=t_month-1).values()
	#Q(date__gte=datetime.now()-timedelta(days=days))|
	leave = Leave.objects.filter(Q(date_approved__gte=datetime.now()-timedelta(days=days)),user=request.user).values()
	
	day = datetime.now().weekday() #0 is monday
	if day == 0:
		attendance = Attendance.objects.filter(user=request.user,date__gte=datetime.now()-timedelta(days=3)).values()
	else:
		attendance = Attendance.objects.filter(user=request.user,date__gte=datetime.now()-timedelta(days=1)).values()
	
	context ={
		'logs':list(log_approval),
		'leave':list(leave),
		'attendance':list(attendance)
	}
	return JsonResponse({'result':context})