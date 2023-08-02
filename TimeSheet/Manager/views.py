from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User,Permission,Group
from .models import InitialPassword,Teams,TeamLeads,TeamUsers
from django.views.decorators.csrf import csrf_exempt
from Authentication.models import Company, userDetails,Employees,userManager
from Attendance.models import Attendance,Leave,TrackAttendance
from datetime import date,datetime
import numpy as np
import re
from emp_worklog.models import worklog
from django.db.models import Sum
from Project.models import Project,SubProject
from Issue.models import Ticket
from django.db.models import Count
from django.core.mail import send_mail
from urllib.parse import quote
from django.conf import settings

# Create your views here.
def send_invite_email(request):
    if request.method == 'POST':
        company_id = Employees.objects.get(user=request.user)
        email = request.POST.get('email')
        company = quote(company_id.company.name)
        # link = "<a href='http://127.0.0.1:8000/validate/addown?email="+email+"&company="+company_id.company.name+"'>Join Company</a>"
        link=f"http://127.0.0.1:8000/validate/addown/?email={email}&company={company}"
        # message = f"Join With Us:\n From Here: '{link}',\n Your Email: '{email}',\n Company Id: '{company_id}'"

        try:
            send_mail(
                "Invitation From Glacier",
                f"Join With Us: {link}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )
            return JsonResponse({'message': 'Invitation sent successfully'})
        except Exception as e:
            return JsonResponse({'message': 'Failed to send invitation'}, status=500)

    return JsonResponse({'message': 'Invalid request'}, status=400)








def getDetails(request):
    allusers =User.objects.all().values('id','username')
    data = {
            'users' :allusers
        }
    return render(request, 'Reports/user_reports.html',data)

def checkTeams(request):
    is_team = False
    #comp = Employees.objects.get(user=request.user)
    #users = Employees.objects.filter(company=request.session['comp'])
    #print(users.user)
    if request.user.is_superuser:
        #users = User.objects.filter(pk__in=users[].user)
        users = Employees.objects.values('user').filter(company=request.session['comp'])
        #print(users)
        is_team=True
    else:
        #u_teams = TeamLeads.objects.values('team').filter(lead=request.user)
        is_manager = userDetails.objects.get(user__id=request.user.id)
        if is_manager.is_manager == True:
            users = userManager.objects.values('user').filter(manager=is_manager)
            is_team=True
        else:
            users = User.objects.filter(username=request.user.username)
        """
        if u_teams.exists():
            is_team=True
            users = TeamUsers.objects.values('user').filter(team__in=u_teams)
        else:
            users = User.objects.filter(username=request.user.username)
        """
    return users,is_team

@csrf_exempt
def getusers(request):
    users =checkTeams(request)

    if request.method == 'POST':
        status = request.POST['status']
        if status == '1': #active
            allusers = User.objects.filter(is_active=True,pk__in=users[0])
        elif status == '2':
            allusers = User.objects.filter(is_active=False,pk__in=users[0])
        else:
            allusers = User.objects.filter(pk__in=users[0])
        
        data = []
        for x in allusers:
            data.append({
                'id':x.id,
                'username':x.username,
                'email':x.email,
                'firstname':x.first_name,
                'lastname':x.last_name,
                'active':x.is_active
            })
        return JsonResponse({'result':data})
    else:
        allusers = User.objects.filter(is_active=True,pk__in=users[0])
        data = {
                'users' :allusers
            }
        #print(data)
        return render(request,'Reports/users.html',data)

def newUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        n_email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        action = request.POST.get('action')
        userId = request.POST.get('id')
        usr = User.objects.filter(username=username).count()
        #print(id)
        if(action == 'create'):
            check = checkPassword(request, pass2)
            if usr != 0 and action == 'create':
                return JsonResponse({'result':"Username alredy exists"})
            elif pass1 != pass2:
                return JsonResponse({'result':"Password didn't match"})
            elif check != 'Success':
                return JsonResponse({'result':check})
            else:
                newUser = User.objects.create_user(username=username,email=n_email,password=pass2)
                #newUser.first_name=fname
                #newUser.last_name =lname
                newUser.save()
                new_user = User.objects.get(username=username)
                #print(new_user.id)
                newP=InitialPassword(user=new_user,first_password=pass1,first_changed=False).save()
                #newP.save()
                attendanceTrack = TrackAttendance(user=new_user,btn1=False,btn2=False,btn3=True).save()
                #attendanceTrack.save()
                comp = Company.objects.get(user =request.user)
                emp = Employees(company=comp,user=new_user).save()

                udetails = userDetails(user=new_user,attendanceType="Physical").save()
                #udetails.save()
                
                return JsonResponse({'result':"Success"})
        elif(action == 'update'):
            User.objects.filter(id=userId).update(username=username,first_name=fname,last_name=lname,email=n_email)
            return JsonResponse({'result':"Successfully Updated"})
    else:
        return render(request,'Reports/users.html')

def updateUser(request,userId):
    getUser = User.objects.get(id=userId)
    data = {
        'users':getUser
    }
    return render(request,'Reports/updateUser.html',data)

def viewUser(request,userId):
    getUser = User.objects.get(id=userId)
    perm = Permission.objects.filter(user=getUser)
    loginType = userDetails.objects.get(user=getUser)
    is_manager=checkTeams(request)

    #print(loginType.attendanceType)
    #user work details
    getMembers = None
    if loginType.is_manager == True:
        udetails = userDetails.objects.get(user=getUser)
        getMembers = userManager.objects.filter(manager=udetails)
        #print(getMembers)

    issue = worklog.objects.filter(User=getUser,TaskType=1).count()
    totalIssue = worklog.objects.filter(TaskType=1).count()
    totalProjectCount = worklog.objects.filter(User=getUser,TaskType=2)
    gettotalProject = worklog.objects.filter(User=getUser,TaskType=2)
    totalProject = []
    for x in gettotalProject:
        if any(dictionary.get('sid') == x.project_id for dictionary in totalProject):
            for index, dictionary in enumerate(totalProject):
                if dictionary.get('sid') == x.project_id:
                    hr = totalProject[index]['hours']
                    hr += x.Hours
                    totalProject[index]['hours']=hr
        else:
            totalProject.append({
                'id':x.project_id.project.id,
                'sid':x.project_id,
                'projectName':x.project_id.project.name,
                'subproject':x.project_id.name,
                'customer':x.project_id.project.customer,
                'leadby':x.project_id.assigned_to.username,
                'managedby':x.project_id.project.manager.username,
                'hours':x.Hours
            })

    project = Project.objects.filter(manager=getUser)
    task =worklog.objects.filter(User=getUser,TaskType=1)
    

    hour = worklog.objects.filter(Billable=True).aggregate(Sum('Hours'))
    totalhour = Attendance.objects.filter(user=getUser).aggregate(Sum('hour'))
    
    leave = Leave.objects.filter(user=getUser).count()
    attendance = Attendance.objects.filter(user=getUser).count()

    groups = Group.objects.all()

    details = {
        'issue':issue,
        'totalIssue':totalIssue,
        'project':project.count(),
        'totalProject':totalProjectCount.count(),
        'hour':hour,
        'totalHour':totalhour,
        'leave':leave,
        'attendance':attendance,
        
    }
    pid = []
    for x in perm:
        pid.append(x.id)
    #print(pid)
    #projects details
    #print(project)
    data = {
        'users':getUser,
        'permissions':pid,
        'summary':details,
        'projects':project,
        'subprojects':totalProject,
        #'hours':totalProject,
        'task':task,
        'loginType':loginType,
        'mfa':loginType.is_mfa,
        'manager':is_manager[1],
        'members':getMembers,
        'groups':groups,
    }
    #print(getUser.last_name)
    return render(request,'Reports/userDetails.html',data)

@csrf_exempt
def addPermissions(request):
    userid = request.POST.get('user')
    permissionId = request.POST.get('pid')
    actn = request.POST.get('action')
    nUser = User.objects.get(id=userid)
    np = Permission.objects.get(id=permissionId)
    if actn == 'add':
        nUser.user_permissions.add(np)
    else:
        nUser.user_permissions.remove(np)
    return JsonResponse({'result':"Success"})


def company(request):
    comp = Company.objects.get(id=1)
    return render(request,'Reports/company.html',{'company':comp})

@csrf_exempt
def report(request):
    user_id = request.POST['user']
    date1 = request.POST['from']
    date2 = request.POST['to']
    user_details = {}
    #print(user_id)
    if user_id != '0':
        user = User.objects.get(id=user_id)
        user_details = {
            'name':user.username,
            'fname':user.first_name,
            'lname':user.last_name,
            'email':user.email,
            'joined':user.date_joined.date(),
            'login':user.last_login.date()
        }

    attendance = Attendance.objects.filter(user=user_id,date__range=(date1,date2)).values()
    leave  = Leave.objects.filter(user=user_id,date__range=(date1,date2)).values()
    days = np.busday_count(date1, date2)
    l_taken =  Leave.objects.filter(user=user_id,date__range=(date1,date2),approval=1).count()
    total = attendance.count()
    a_details = {
        'worked':str(total),
        'total':str(days),
        'leave':str(l_taken)
    }
    #new_data = attendance.union(leave)
    #print(a_details)
    data={
        'user':user_details,
        'attendance':list(attendance),
        'leave':list(leave),
        'atdnc':a_details
    }
    #print(attendance)
    return JsonResponse(data)

def checkPassword(request,password):
    password = password
    flag = ''
    while True:
        if (len(password)<=8):
            flag = 'Password must contain 8 characters!'
            break
        elif not re.search("[a-z]", password):
            flag = 'Password must contain [a-z] characters!'
            break
        elif not re.search("[0-9]", password):
            flag = 'Password must contain numbers[0-9] characters!'
            break
        elif not re.search("[_@$!]" , password):
            flag = 'Password must contain one special characters!'
            break
        else:
            flag = 'Success'
            break
    return flag

@csrf_exempt
def updateLoginType(request):
    print('Success')
    l_type = request.POST.get('action')
    typeTo = request.POST.get('type')
    userid = request.POST.get('user')
    user = User.objects.get(id=userid)
    
    if l_type == 'update':
        userDetails.objects.filter(user=user).update(attendanceType=typeTo)
        if typeTo == 'Physical':
            userDetails.objects.filter(user=user).update(mrequest=False)
    elif l_type == 'request':
        userDetails.objects.filter(user=user).update(mrequest=True)
    else:
        if typeTo == 'True':
            userDetails.objects.filter(user=user).update(is_mfa=False)
        else:
            userDetails.objects.filter(user=user).update(is_mfa=True)
        
    return JsonResponse({'result':'success'})

@csrf_exempt
def addManagerMember(request):
    userList = request.POST.getlist('userlist[]')
    id = userList[0]
    userList.remove(id)

    userDetails.objects.filter(user__id=id).update(is_manager=True)
    
    for u in userList:
        user = User.objects.get(username=u)
        checkUser = userManager.objects.filter(manager__user__id=id,user=user)
        
        if checkUser.exists() == False:
            manager = userDetails.objects.get(user__id=id) 
            userManager(manager=manager,user=user).save()
            
    return JsonResponse({'result':'success'})




@csrf_exempt
def removeMember(request):
    manager = request.POST.get('manager')
    user = request.POST.get('user')
    userManager.objects.filter(manager__user__id=manager,user__username=user).delete()
    return JsonResponse({'result':user})

@csrf_exempt
def removeManager(request):
    userid = request.POST.get('id')
    userDetails.objects.filter(user__id=userid).update(is_manager=False)
    userManager.objects.filter(manager__user__id=userid).delete()
    return JsonResponse({'result':'success'})