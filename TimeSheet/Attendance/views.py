from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect, HttpResponse
from Attendance.models import Attendance, Leave, LeaveType,User,TrackAttendance
from Authentication.models import userDetails,Company,Employees
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import datetime
from geopy.geocoders import Nominatim
from django.db.models import Sum,Q
from math import radians, cos, sin, asin, sqrt
from Manager.views import checkTeams
#for email send
from django.core.mail import send_mail
from django.conf import settings
# email 

# new add
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def attendance(request):
    if request.user.is_authenticated:
        #comp = request.session['comp']
        #user = Employees.objects.filter(company=comp).values('user')
        #allusers =User.objects.filter(pk__in=user).values('id','username')

        getTeam_users = checkTeams(request)
        allusers = User.objects.filter(pk__in=getTeam_users[0])

        #btnTrack=TrackAttendance.objects.get(user=request.user)
        attenType = userDetails.objects.get(user=request.user)
        #print(attenType.attendanceType)
        #send_mail('A cool subject', 'A stunning message', settings.EMAIL_HOST_USER, ['anilrajbanshi31@gmail.com'])
        #getDistance(request) #distance calculator
        date = datetime.date.today()
        if request.user.is_superuser:
            result = Attendance.objects.filter(date__year=date.year,date__month =date.month,user=request.user) # 1=january
        else:
            result = Attendance.objects.filter(date__year=date.year,date__month =date.month, user=request.user)
        #print(result)
        gettoday = Attendance.objects.filter(user=request.user,date=date)
        #print(gettoday.first())
        if gettoday.first() != None:
            today = gettoday.first()
        else :
            today = "None"
        data = {
            'result': result,
            'users' :allusers,
            #'btn' :btnTrack,
            'attendanceType':attenType,
            'today':today
        }
        return render(request, 'Attendance/attendance.html',data)
    else:
        return HttpResponseRedirect(reverse('login'))

def getTodayAttendance(request):
    data = Attendance.objects.filter(date=datetime.date.today(),user=request.user).values()
    return JsonResponse({'result':list(data)})

def getTodayAll(request):
    data = Attendance.objects.filter(date=datetime.date.today()).values()
    return JsonResponse({'result':list(data)})

@csrf_exempt
def getAttendance(request):
    month = request.POST['month']
    year = request.POST['year']
    user_id =request.POST.get('user')
    #print(user_id)
    if user_id == '0':
        result = Attendance.objects.filter(date__month=month,date__year=year)
    elif user_id == None:
        result = Attendance.objects.filter(date__month=month,date__year=year,user=request.user)
    else:
        result = Attendance.objects.filter(date__month=month,date__year=year,user=user_id)
    
    alldata = getUsernames(request,result)
    return JsonResponse({'attendance':alldata})

#def attendance_Details(request,attendance_id):
def attendance_Details(request):
    attendance_id=request.POST.get('id')
    attendance = Attendance.objects.get(id=attendance_id)
    if attendance.start_location != '':
        start_location = getLocation_Name(attendance.start_location)
    else:
        start_location="Location Not Saved"
    if attendance.stop_location != '':
        stop_location = getLocation_Name(attendance.stop_location)
    else:
        stop_location="Location Not Saved"
    new_data = Attendance()
    new_data.date=attendance.date
    new_data.day=attendance.day
    new_data.entry=attendance.entry
    new_data.lbreak1 =attendance.lbreak1
    new_data.lbreak2 = attendance.lbreak2
    new_data.exit = attendance.exit
    new_data.start_location =start_location
    new_data.stop_location=stop_location
    
    #return render(request,'Attendance/attendance_details.html',{'data':new_data})
    return JsonResponse({'start':str(new_data.start_location),'stop':str(new_data.stop_location)})

@csrf_exempt
def make_attendance(request):
    btn = request.POST['btn']
    date = request.POST.get('date')
    check_date = Attendance.objects.filter(date=date,user=request.user).exists()
    day = request.POST.get('day')
    entry = request.POST.get('entry')
    lbreak1 = request.POST.get('lbreak1')
    lbreak2 = request.POST.get('lbreak2')
    exit = request.POST.get('exit')
    hour = request.POST.get('hour')
    start_location = request.POST.get('start_location')
    stop_location = request.POST.get('stop_location')
    if check_date == True:
        g_data = Attendance.objects.get(date=date, user=request.user)
        if lbreak1 != None:
            Attendance.objects.filter(id=g_data.id).update(lbreak1 = lbreak1)
            TrackAttendance.objects.filter(user=request.user).update(btn2=True)
        if lbreak2 != None:
            Attendance.objects.filter(id=g_data.id).update(lbreak2 = lbreak2)
            TrackAttendance.objects.filter(user=request.user).update(btn2=False)
        if exit != None:
            #attendance = Attendance(id=g_data.id,user=g_data.user,date=g_data.date,day=g_data.day,entry=g_data.entry,lbreak1=g_data.lbreak1,lbreak2=g_data.lbreak2,exit=exit,hour=hour,start_location=g_data.start_location,stop_location=stop_location)
            Attendance.objects.filter(id=g_data.id).update(exit = exit,hour=hour, stop_location =stop_location)
            TrackAttendance.objects.filter(user=request.user).update(btn3=True,btn1=False)
        #attendance.save()
    else:
        attendance = Attendance(user=request.user,day=day,entry=entry,start_location=start_location)
        TrackAttendance.objects.filter(user=request.user).update(btn1=True,btn3=False)
        attendance.save()

    check_date = datetime.date.today()
    if request.user.is_superuser:
        getAll=Attendance.objects.filter(date__year=check_date.year,date__month=check_date.month,user=request.user)
        alldata = getUsernames(request,getAll)
    else:
        getAll=Attendance.objects.filter(date__year=check_date.year,date__month=check_date.month,user=request.user).values()
        alldata=list(getAll)
    
    return JsonResponse({'attendance':alldata})

def getUsernames(request,result):
    if request.user.is_superuser:
        #print(result)
        alldata =[]
        for x in result:
            alldata.append({
                'id':x.id,
                'date':x.date,
                'day':x.day,
                'user':x.user.username,
                'entry':x.entry,
                'lbreak1':x.lbreak1,
                'lbreak2':x.lbreak2,
                'exit':x.exit,
                'hour':x.hour
            })
    else:
        alldata = list(result.values())
    
    return alldata

@login_required
@csrf_exempt
def checkLeave(request):
    d_date = datetime.datetime.now()
    id=request.POST.get('id')
    count = LeaveType.objects.get(id=id)
    leave = Leave.objects.filter(type=count,date__year=d_date.year,date__month=d_date.month,user=request.user)
    print(leave.count())
    return JsonResponse({'available':count.days,'taken':leave.count()})

@login_required
def getleave(request):
    #all_leaves = Leave.objects.all()
    usr = checkTeams(request)
    allusers =User.objects.filter(pk__in=usr[0]).values('id','username')
    all_leaves = Leave.objects.filter(user__id__in=usr[0])
    
    type = LeaveType.objects.all().values()
    return render(request, 'Attendance/leave.html',{'result':all_leaves,'users' :allusers,'LeaveTypes':type})

def request_leave(request):
    type= request.POST['type']
    leave_from = request.POST['leave_from']
    leave_to = request.POST['leave_to']
    details = request.POST['details']
    leaveType = LeaveType.objects.get(id=type)
    id = request.POST['id']
    if id != "":
        Leave.objects.filter(id=id).update(user = request.user,type=leaveType,leave_from=leave_from,leave_to=leave_to,details=details)
    else:
        Leave(user = request.user,type=leaveType,leave_from=leave_from,leave_to=leave_to,details=details).save()
        
    if request.user.is_superuser:
        result = Leave.objects.all()
    else:
        result = Leave.objects.filter(user=request.user)

    getmanager = userDetails.objects.get(user__id=request.user.id)
    if getmanager.is_manager == True or request.user.is_superuser:
        manager = True
    else: 
        manager = False
    list_data = []
    for x in result:
        list_data.append({
            'date':x.date,
            'user':x.user.username,
            'type':x.type.name,
            'leave_from':x.leave_from,
            'leave_to':x.leave_to,
            'details':x.details,
            'approval':x.approval.name
        })
    #data = list(result)
    #print(list_data)
    return JsonResponse({'result':list_data,'is_manager':manager})

def getLocation_Name(user_location):
    if user_location != None:
        geolocator = Nominatim(user_agent="geoapiExercises")
        new_location = user_location.split(",")
        Latitude = new_location[0]
        Longitude = new_location[1]
        location = geolocator.reverse(Latitude+","+Longitude)
        address = location.raw['address']
        city = address.get('city', '')
        street = address.get('street_name','')
        state = address.get('state', '')
        country = address.get('country', '')
        code = address.get('country_code')
        zipcode = address.get('postcode')
        #print(location)
        return location
    else:
        return 'Location Disabled'
@login_required
@csrf_exempt
def getLeave(request):
    status = request.POST.get('status')
    user_id = request.POST.get('user')
    usr = checkTeams(request)
    print(user_id)
    if user_id == '0':
        if status == '0':
            result = Leave.objects.filter(user__id__in=usr[0])
        else:
            result = Leave.objects.filter(approval = status,user__id__in=usr[0])
    elif user_id == None:
        if status=='0':
            result = Leave.objects.filter(user=request.user)
        else:
            result = Leave.objects.filter(approval = status, user=request.user)
    elif status =='0':
        result = Leave.objects.filter(user=user_id)
    else:
        result = Leave.objects.filter(approval=status,user=user_id)

    all_leaves = getUsernamesForLeave(request, result)
    getmanager = userDetails.objects.get(user__id=request.user.id)
    if getmanager.is_manager == True or request.user.is_superuser:
        manager = True
    else: 
        manager = False
    return JsonResponse({'result':all_leaves,'is_manager':manager})

def getUsernamesForLeave(request,result):
    if request.user.is_superuser:
        alldata =[]
        for x in result:
            alldata.append({
                'id':x.id,
                'date':x.date,
                'type':x.type.name,
                'user':x.user.username,
                'details':x.details,
                'leave_from':x.leave_from,
                'leave_to':x.leave_to,
                'approval':x.approval.name
            })
    else:
        alldata =[]
        for x in result:
            alldata.append({
                'id':x.id,
                'date':x.date,
                'type':x.type.name,
                'user':x.user.username,
                'details':x.details,
                'leave_from':x.leave_from,
                'leave_to':x.leave_to,
                'approval':x.approval.name
            })
    
    return alldata

@csrf_exempt
def LeaveDetails(request):#leave_id):
    #leave = Leave.objects.get(id=leave_id)
    is_manager = checkTeams(request)

    id=request.POST.get('id')
    leave = Leave.objects.filter(id=id).values()
    #return render(request, 'Attendance/leaveDetails.html',{'leave':leave})
    return JsonResponse({'result':list(leave),'is_manager':is_manager[1]})

@csrf_exempt
def getLeaveDetails(request,leave_id):
    leave = Leave.objects.get(id=leave_id)
    return render(request, 'Attendance/leaveDetails.html',{'leave':leave})

@csrf_exempt
def updateLeave(request):
    approval =request.POST['status']
    leave = request.POST['leave_id']
    date = datetime.datetime.now()
    #print(date)
    Leave.objects.filter(id=int(leave)).update(approval=approval,date_approved=date,approved_by=str(request.user.username))

    return JsonResponse({'result':'Successfully Updated'})


def getLeaveCount(request):
    approved = Leave.objects.filter(approval=1).count()
    pending = Leave.objects.filter(approval=2).count()
    declined = Leave.objects.filter(approval=3).count()

    return JsonResponse({'app':approved,'pend':pending,'dec':declined})

def getattendanceCount(request):
    usr =checkTeams(request)
    approved = Leave.objects.filter(approval=1,user__id__in=usr[0]).count()
    users = User.objects.filter(pk__in=usr[0]).count()
    attendance = Attendance.objects.filter(date__month=datetime.date.today().month,user__id__in=usr[0]).count()
    #print(attendance)
    return JsonResponse({'onLeave':approved,'users':users,'active':attendance})


def attendancebyUser(request):
    approved = Leave.objects.filter(approval=1).count()
    attendance = Attendance.objects.filter(date__month=datetime.date.today().month).count()
    #print(attendance)
    return JsonResponse({'onLeave':approved,'active':attendance})




@csrf_exempt
def updateLeaveType(request):
    if request.method=="POST":
        action = request.POST.get('action')
        name = request.POST.get('name')
        days = request.POST.get('day')
        id = request.POST.get('id')
        if action == "add":
            getname = LeaveType.objects.filter(name=name).exists()
            if getname == True:
                return JsonResponse({'result':"Leave Type already exists!"})
            else:
                LeaveType(name=name,days=days).save()
                return JsonResponse({'result':"Leave Added Successfully!"})
        elif action == "edit":
            LeaveType.objects.filter(id=id).update(name=name,days=days)
            return JsonResponse({'result':"Update Successfully!"})
        else:
            LeaveType.objects.get(id=id).delete()
            return JsonResponse({'result':"Deleted Successfully!"})
    else:
        return JsonResponse({'result':"Something Went Wrong!"})

@csrf_exempt
def getLeaveType(request):
    id = request.POST.get('id')
    print(id)
    leave=LeaveType.objects.get(id=id)
    return JsonResponse({'result':leave.days})


def getDistance(request):
    #LoA = radians(LoA) 
    #LoB = radians(LoB) 
    #LaA= radians(LaA) 
    #LaB = radians(LaB)


    #test by anil 
    LaA = 38.63
    LaB = 39.95
    LoA = -90.19
    LoB = -75.14
    # The "Haversine formula" is used.
    D_Lo = LoB - LoA
    D_La = LaB - LaA
    P = sin(D_La / 2)**2 + cos(LaA) * cos(LaB) * sin(D_Lo / 2)**2 
   
    Q = 2 * asin(sqrt(P))  
    # The earth's radius in kilometers.
    R_km = 6371 
    # Then we'll compute the outcome.
    print ("The distance between St Louis and Philadelphia is: ", Q * R_km, "K.M") 
    #return(Q * R_km)
    return True

    LaA = 38.63
    LaB = 39.95
    LoA = -90.19
    LoB = -75.14
    print ("The distance between St Louis and Philadelphia is: ", distance_d(LaA, LaB, LoA, LoB), "K.M") 

