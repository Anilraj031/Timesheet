from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.models import User,Permission,Group
from .models import InitialPassword,Teams,TeamLeads,TeamUsers
from django.views.decorators.csrf import csrf_exempt
from Authentication.models import Company, userDetails,Employees,userManager
from Attendance.models import Attendance,Leave,TrackAttendance
from Customer.models import customer,employee
from datetime import date,datetime,timedelta
from django.db.models import Q
from dateutil.relativedelta import relativedelta,MO
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
from django.contrib.auth.decorators import login_required
from dateutil.parser import parse
import pandas as pd
import xlwt


# Create your views here.
def send_invite_email(request):
    if request.method == 'POST':
        company_id = Employees.objects.get(user=request.user)
        email = request.POST.get('email')
        company = quote(company_id.company.name)
        # link = "<a href='http://127.0.0.1:8000/validate/addown?email="+email+"&company="+company_id.company.name+"'>Join Company</a>"
        link=f"http://127.0.0.1:8000/validate/addown/?email={email}&company={company}"
        # message = f"Join With Us:\n From Here: '{link}',\n Your Email: '{email}',\n Company Id: '{company_id}'"
        print('I am here')
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







@login_required
def getDetails(request):
    get_users = checkTeams(request)
    allusers = User.objects.filter(pk__in=get_users[0]).values('id','username')
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
            users1 = userManager.objects.values('user').filter(manager=is_manager)

            users = User.objects.filter(Q(pk__in=users1)| Q(pk=request.user.id))
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

@login_required
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
                newUser = User.objects.create_user(username=username,email=n_email,password=pass2).save()

                new_user = User.objects.get(username=username)

                newP=InitialPassword(user=new_user,first_password=pass1,first_changed=False).save()

                #attendanceTrack = TrackAttendance(user=new_user,btn1=False,btn2=False,btn3=True).save()
                comp = Company.objects.get(user =request.user)
                emp = Employees(company=comp,user=new_user).save()

                udetails = userDetails(user=new_user).save()
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

@login_required
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
    issue_hours = worklog.objects.filter(User=request.user,Billable=True,TaskType=1,Date__range=(date1,date2)).aggregate(Sum('Hours'))
    project_hours = worklog.objects.filter(User=request.user,Billable=True,TaskType=2,Date__range=(date1,date2)).aggregate(Sum('Hours'))
    other_hours = worklog.objects.filter(User=request.user,Billable=False,Date__range=(date1,date2)).aggregate(Sum('Hours'))

    print(other_hours)
    issues = Ticket.objects.filter(assigned_to__id=user_id).values()

    data={
        'user':user_details,
        #'attendance':list(attendance),
        'leave':list(leave),
        'atdnc':a_details,
        'issue_hr':issue_hours,
        'project_hr':project_hours,
        'other_hr':other_hours,
        'issue':list(issues),
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

@login_required
def invoice(request):
    usr = checkTeams(request)
    users = User.objects.filter(pk__in=usr[0])
    cutomers = customer.objects.all()
    return render(request,'Reports/invoice.html',{'customer':cutomers,'users':users})

def getInvoice(request):
    customer_id = request.GET['customer']
    month = request.GET['month']
    invoice = createInvoice(month,customer_id)

    return JsonResponse({'result':invoice[0],'details':invoice[1]})

def createInvoice(month,customer_id):

    start_date = getWeekNum(month,None,1)
    end_date = getWeekNum(month,None,2)


    custr = customer.objects.get(id=customer_id)
    customer_contacts = employee.objects.filter(company__id=customer_id)
    issue = Ticket.objects.filter(affected_user__in=customer_contacts)
    projects = Project.objects.filter(customer = custr.name)
    subProjects = SubProject.objects.filter(project__in=projects)

    logs = worklog.objects.filter(Q(task__in=issue)|Q(project_id__in=subProjects),Billable=True,Date__range=(start_date,end_date)).order_by('Date')

    #hours
    projecthr = worklog.objects.filter(project_id__in=subProjects,Billable=True,Date__range=(start_date,end_date)).aggregate(Sum('Hours')).get('Hours__sum', 0.00)
    issueHr = worklog.objects.filter(task__in=issue,Billable=True,Date__range=(start_date,end_date)).aggregate(Sum('Hours')).get('Hours__sum', 0.00)
    totalHr = logs.aggregate(Sum('Hours')).get('Hours__sum', 0.00)
    cname = custr.name

    hrs = {
        'project':projecthr,
        'issue':issueHr,
        'total':totalHr,
        'customer':cname
    }


    invoice = []
    for l in logs:
        weekNum = getWeekNum(month,l.Date,3)
        if l.task != None:
            name = l.task.ticket_name
        else:
            name = l.project_id.project.name
        invoice.append({
            'user':l.User.username,
            'week':'Week '+str(weekNum),
            'date':str(l.Date),
            #'issue':l.task.ticket_name,
            'issue':name,
            'hour':l.Hours,
            'detail':l.Workdone,
            })
    """
    for p in projectLogs:
        weekNum1 = getWeekNum(month,p.Date,3)
        invoice.append({
            'user':p.User.username,
            'week':weekNum1,
            'date':str(p.Date),
            'issue':p.project_id.project.name,
            'hour':p.Hours,
            'detail':p.Workdone,
        })
    """
    #print(projectLogs)
    #print(end_date)

    return invoice,hrs

def getWeekNum(month,date1,type):
    year  = int(datetime.today().year)
    first_date = datetime(year, int(month), 1)

    if month == 12:
        last_date = datetime(year, int(month), 31)
    else:
        last_date = datetime(year, int(month) + 1, 1) + timedelta(days=-1)

    #last monday is start date if today is monday lastMonday is today
    lastMonday = first_date + relativedelta(weekday=MO(-1))
    nextMonday = last_date + relativedelta(weekday=MO(1))


    if nextMonday.day > 1:
        end_date = (last_date + relativedelta(weekday=MO(-1)))-timedelta(days=1)
    else:
        end_date = nextMonday-timedelta(days=1)

    week1 = first_date + relativedelta(weekday=MO(-1))
    week2 = (week1+timedelta(days=1)) + relativedelta(weekday=MO(1))
    week3 = (week2+timedelta(days=1)) + relativedelta(weekday=MO(1))
    week4 = (week3+timedelta(days=1)) + relativedelta(weekday=MO(1))
    week5 = (week4+timedelta(days=1)) + relativedelta(weekday=MO(1))

    #print(date1)
    #print(week4)
    if type == 1:
        return lastMonday #as start date for selected month
    elif type == 2:
        return end_date
    else:
        date2 = (convert_to_datetime(str(date1))).date()
        #print(date2)
        #print("sda")
        date = datetime(date2.year,date2.month,date2.day)
        w1 = datetime(week1.year,week1.month,week1.day)
        w2 = datetime(week2.year,week2.month,week2.day)
        w3 = datetime(week3.year,week3.month,week3.day)
        w4 = datetime(week4.year,week4.month,week4.day)
        w5 = datetime(week5.year,week5.month,week5.day)
        #print(date)
        #print(w1)
        if date >= w1 and date < w2:
            return 1
        elif date >= w2 and date < w3:
            return 2
        elif date >= w3 and date < w4:
            return 3
        elif date >= w4 and date < w5:
            return 4
        elif date >=w5 and date < datetime(end_date.year,end_date.month,end_date.day):
            return 5
        else:
            return None

def convert_to_datetime(input_str, parserinfo=None):
    return parse(input_str, parserinfo=parserinfo)

@csrf_exempt
def download_invoice_data(request):
    id = request.GET.get('id')
    month = request.GET.get('month')
    #print('I am id'+id)
    get_data = createInvoice(month,id)
    data = get_data[0]

    #print(get_data[1])

    #print(data)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Invoice.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Log Data') # this will make a sheet named Users Data

    #hours details
    font_style1 = xlwt.XFStyle()
    font_style1.font.bold = True
    ws.write_merge(0, 0, 0, 1, 'Customer',font_style1)
    ws.write(0, 2, get_data[1]['customer'],font_style1)
    ws.write_merge(1, 1, 0, 1, 'Total Hr',font_style1)
    ws.write(1, 2, get_data[1]['total'],font_style1)

    #ws.write_merge(0, 0, 0, 1, 'Long Cell')
    # Sheet header, first row
    row_num = 3
    #column width
    col_width = 256*15
    ws.col(0).width = col_width
    ws.col(1).width = 256*10
    ws.col(2).width = col_width
    ws.col(3).width = col_width
    ws.col(4).width = 256*10
    ws.col(5).width = 256*40

    #styling color blue
    xlwt.add_palette_colour("custom_blue_color", 0x21) # the second argument must be a number between 8 and 64
    wb.set_colour_RGB(0x21, 79, 129, 189) # Red — 79, Green — 129, Blue — 189
    #font_style = xlwt.XFStyle()
    font_style = xlwt.easyxf('pattern: pattern solid, fore_colour custom_blue_color')
    font_style.font.bold = True

    #styling left align
    style_text_align_vert_bottom_horiz_left = xlwt.easyxf("align: vert bottom, horiz left")



    columns = ['Username', 'Week','Date', 'Title','Hour','Details']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    #rows = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')

    rows = data
    """
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    """
    columns = list(data[0].keys()) # list() is not need in Python 2.x
    for i, row in enumerate(data):
        for j, col in enumerate(columns):
            ws.write(i+4, j, row[col],style_text_align_vert_bottom_horiz_left)

    wb.save(response)

    return response