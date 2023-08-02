from django.shortcuts import render, redirect
# from django.http import HttpResponse
from .models import worklog,tasktype,LogApproval
from Project.models import Project, SubProject
from Issue.models import Ticket
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import JsonResponse,HttpResponse
from django.db.models import Q
from dateutil.relativedelta import relativedelta,MO
from django.db.models import Sum
from django.contrib.auth.models import User
from Customer.models import customer
from Manager.views import checkTeams
from Manager.models import FilterQuery
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import xlwt

# Create your views here.
def dailylog1(request):
    all_data=worklog.objects.all()
    context= {
        'all_data':all_data
    }
    print(context)
    return render(request, 'dailylog1.html', context)

def billable(request):
    return render(request, 'billable.html')

def nonbillable(request):
    return render(request, 'non_billable.html')

def index(request):
    return render(request, 'index.html')

def loginpage(request):
    return render(request, 'loginpage.html')

def test(request):
    return render(request, 'test.html')

def enterrecord(request):
    return render(request, 'enterrecordform.html')

def addrecord(request):
    return render(request, 'addrecord.html')

@csrf_exempt
def dailylog(request):
    #view list of users if users is admin or team leader
    getTeam_users = checkTeams(request)
    allusers = User.objects.filter(pk__in=getTeam_users[0])
    
    task =tasktype.objects.all().values()

    date = datetime.today().weekday()
    if date == 0: #0=monday
        today = datetime.today()#-timedelta(days=1)#datetime.today()
    else:
        today = datetime.today()
    lastMonday = today + relativedelta(weekday=MO(-1))
    nextMonday = today + relativedelta(weekday=MO(1))
    
    
    all_data=worklog.objects.filter(User = request.user,Date__month=today.month)
    #all_data=worklog.objects.filter(User = request.user)
    # pagination
    paginator=Paginator(all_data,10)
    page_number=request.GET.get('page')
    page_datafinal=paginator.get_page(page_number)
    totalpage=page_datafinal.paginator.num_pages

    if request.method == 'POST':
        user = request.POST.get('id')
        thisweekdata = worklog.objects.filter(User = user,Date__range=(lastMonday,nextMonday))
        #for last weeks log
        lastMonday2 = today + relativedelta(weekday=MO(-2))
        lastweekdata = worklog.objects.filter(User = user,Date__range=(lastMonday2,lastMonday-timedelta(days=1)))
        context= {
            'all_data':list(all_data.values()), 
            'tasktype':list(task),
            'lastweekdata':get_Projectnames(request,lastweekdata),
            'lastweektotal':lastweekdata.aggregate(Sum('Hours')),
            'thisweekdata':get_Projectnames(request,thisweekdata),
            'thisweektotal':thisweekdata.aggregate(Sum('Hours')),
            
        }

        return JsonResponse({'result':context})
    
    if request.method == 'GET':
        thisweekdata = worklog.objects.filter(User = request.user,Date__range=(lastMonday,nextMonday))
        #print(thisweekdata[0].Date)
        #for last weeks log
        lastMonday2 = today + relativedelta(weekday=MO(-2))
        lastweekdata = worklog.objects.filter(User = request.user,Date__range=(lastMonday2,lastMonday-timedelta(days=1)))
        context= {
            'all_data':all_data, 
            'tasktype':task,
            'lastweekdata':lastweekdata,
            'lastweektotal':lastweekdata.aggregate(Sum('Hours')),
            'thisweekdata':thisweekdata,
            'thisweektotal':thisweekdata.aggregate(Sum('Hours')),
            'is_team':getTeam_users[1],
            # pagination
            'all_data':page_datafinal,
            'totalpage':[n+1 for n in range(totalpage)],
            'users':allusers
        }
        #print(getTeam_users[1])
        return render(request, 'dailylog.html', context)
        
#jquery filed name display
def get_Projectnames(request,result):
    #print(result[1].Date)
    data = []
    for d in result:
        data.append({
            'date':''+d.Date.strftime("%B %d, %Y"),
            'project': get_project_or_task_empty(request,d.project_id_id,'project'),
            'tasktype':get_project_or_task_empty(request,d.TaskType.id,'tasktype'),
            'task':get_project_or_task_empty(request,d.task_id,'task'),
            'priority': get_project_or_task_empty(request,d.task_id,'priority'),
            'hours':d.Hours,
            'billable':d.Billable,
            'id':d.id
        })
    #print(data)
    return data

def get_project_or_task_empty(request,id,type):
    #print(id)
    name = 'none'
    if type =='tasktype':
        if id != None:
            name1 = tasktype.objects.get(id=id)
            name = name1.TaskType
    elif type == 'project':
        if id != None:
            name1 = SubProject.objects.get(id=id)
            name=name1.name
    elif type =='task':
         if id != None:
            name1 = Ticket.objects.get(id=id)
            name=name1.ticket_name
    else:
        if id != None:
            name1 = Ticket.objects.get(id=id)
            name=name1.priority
    return name

# This is for adding record
def ADD(request):
    if request.method == "POST":
        date =request.POST.get('date')
        tasktype =request.POST.get('tasktype')
        project_id = request.POST.get('sublist')
        task_id = request.POST.get('issue_list')
        workdone =request.POST.get('workdone')
        hours =int(request.POST.get('hours'))
        billable =request.POST.get('billable')
        action = request.POST.get('action')
        id=request.POST.get('id')

        if billable == 'on' or billable == 'true': 
            b1=True 
        else:
            b1=False
        
        print('i am herer')
        if project_id != None:
            project = SubProject.objects.get(id=project_id)
        else:
            project = None

        if task_id != None:
            task = Ticket.objects.get(id=task_id)
        else:
            task = None
        
        if action == 'update':
            worklog.objects.filter(id=id).update(Date=date,TaskType_id=tasktype,project_id=project,task=task,Workdone=workdone,Hours=hours,Billable=b1)
        if action == 'updateManager':
              worklog.objects.filter(id=id).update(Workdone=workdone,Hours=hours,Billable=b1)
        else:
            datas = worklog (
                User = request.user ,
                Date = date,
                TaskType_id = tasktype,
                project_id = project,
                task = task,
                Workdone = workdone,
                Hours = hours,
                Billable = b1
            )
            datas.save()
        return redirect('dailylog')

# This is for editing record
def Edit(request):
    logId = request.GET.get('id')
    data=worklog.objects.filter(id=logId).values()

    return JsonResponse({'result':list(data)})

# This is for updating record
def Update(request,id):
    if request.method == "POST":
        user=request.POST.get('user')
        date=request.POST.get('date')
        tasktype=request.POST.get('tasktype')
        workdone=request.POST.get('workdone')
        hours=int(request.POST.get('hours'))
        billable=request.POST.get('billable')

        if billable == 'on': 
            b1=True 
        else:
            b1=False

        datas = worklog (
            id = id,
            User = user,
            Date = date,
            TaskType_id = tasktype,
            Workdone = workdone,
            Hours = hours,
            Billable = b1
        )
        datas.save()
        return redirect('dailylog')
    return redirect(request,'dailylog.html')

# This is for deleting record
def Delete(request,id):
    all_data=worklog.objects.filter(id = id)
    all_data.delete()
    return redirect('dailylog')

def gets(request):   
    task_id=request.GET.get('task')
    #print(task_id)   
    if task_id == '1':
        data=Ticket.objects.filter(Q(state='New')| Q(state='InProgress'),company=request.session['comp']).values()
    elif task_id == '2':
        data=Project.objects.all().values()
    else:
        data=""
    return JsonResponse({'result':list(data)})

def subproject(request):
    id=request.GET['id']
    subdata=SubProject.objects.filter(project=id).values()
    # print(request.user)
    return JsonResponse({'result':list(subdata)})


def getMonthlyHours(request):
    year = datetime.today().year
    month = datetime.today().month
    
    data = {}
    keys = range(1,13)
    for i in keys:
        data[i] = worklog.objects.filter(Date__year =year,Date__month= i,Billable=True).aggregate(Sum('Hours'))

    result={
        'year':year,
        'test':data
    }
    return JsonResponse(result)


def getHoursData(request):
    usr = checkTeams(request)
    #gethour = customer.objects.all().aggregate(Sum('contract_hr')).get('contract_hr__sum', 0.00)
    gethour = usr[0].count()*40
    users = User.objects.filter(pk__in=usr[0])
    usr_hour = []
    for x in users:
        usr_hour.append({
            'user':x.username,
            'hour':worklog.objects.filter(Date__month=datetime.today().month,User = x.id,Billable=True).aggregate(Sum('Hours')).get('Hours__sum', 0.00),
        })
    #print(usr_hour)
    achievedhr = worklog.objects.filter(Date__month=datetime.today().month,Billable=True,User__id__in=usr[0]).aggregate(Sum('Hours')).get('Hours__sum', 0.00)
    nonbillable = worklog.objects.filter(Date__month=datetime.today().month,Billable=False,User__id__in=usr[0]).aggregate(Sum('Hours')).get('Hours__sum', 0.00)
    return JsonResponse({'requiredHr':gethour,'users':usr_hour,'hour':achievedhr,'nonBillable':nonbillable})



def usersLog(request):
    getTeam_users = checkTeams(request)
    allusers = User.objects.filter(pk__in=getTeam_users[0])
    task =tasktype.objects.all().values()
    team = checkTeams(request)
    context={
        'users' : allusers,
        'task' :task,
        'is_team':team[1],
    }
    return render(request, 'AllLog.html', context)

@csrf_exempt
def getLogByUsers(request):
    if request.method =='POST':
        id = request.POST.get('user')
        start_date = request.POST.get('from')
        end_date = request.POST.get('to')
        log = request.POST.get('log')
        task = request.POST.get('task')
        if id == None:
            id=request.user.id
        data = createReportData(id,start_date,end_date,log,task)
        user=User.objects.get(pk=id)
        FilterQuery(type='worklog',user=user,date1=start_date,date2=end_date,task_type=task,log_type=log).save()
        f_id=FilterQuery.objects.last()

    return JsonResponse({'result':data,'filter':f_id.id})


def createReportData(id,start_date,end_date,log,task):
    if log == 'None' and task =='None':
        data = worklog.objects.filter(User__id=id,Date__range=(start_date,end_date))
    elif task =='None' or log =='None':
        if task == 'None':
            data = worklog.objects.filter(User__id=id,Date__range=(start_date,end_date),Billable=log)
        else: 
                data = worklog.objects.filter(User__id=id,Date__range=(start_date,end_date),TaskType=task)
    else: 
        data = worklog.objects.filter(User__id=id,Date__range=(start_date,end_date),Billable=log,TaskType=task)
    
    readable_data = []
    for d in data:
        taskname = 'None'
        if d.TaskType_id == 1:
            taskname = d.task.ticket_name
        if d.TaskType_id == 2:
            taskname = d.project_id.name
        readable_data.append({
            'id':d.id,
            'user':d.User.username,
            'date':str(d.Date),
            'task':d.TaskType.TaskType,
            'taskname':taskname,
            'billable':d.Billable,
            'details':d.Workdone,
            'hour':d.Hours,
        })
    return readable_data
"""
@csrf_exempt
def getLogByUsers(request):
    if request.method =='POST':
        u_id = request.POST.get('id')

    return JsonResponse({'result':'success'})
"""
@csrf_exempt
def download_excel_data1(request,id):
    if request.method =='POST':
        id = request.POST.get('user')
        start_date = request.POST.get('from')
        end_date = request.POST.get('to')
        log = request.POST.get('log')
        task = request.POST.get('task')
        user = User.objects.get(id=id)

        """file is created on local machine"""
        print('i am here')
        data = createReportData(id,start_date,end_date,log,task)
        #pd.DataFrame(data).to_excel('Log_Report_'+user.username+'_'+start_date+'.xlsx')
        #df = pd.DataFrame({'user': data.user, 'date': data.date, 'details': data.details, 'taskname': data.taskname,'tasktype':data.task,'hour':data.hour,'billable':data.billable})
        df = pd.DataFrame(data)
        writer = pd.ExcelWriter('Log_Report_'+user.username+'_'+start_date+'_to_'+end_date+'.xlsx')
        df.to_excel(writer, sheet_name='Sheet1', startrow=1, index=False) 
        worksheet = writer.sheets['Sheet1']
        worksheet.write_string(0, 3, 'Employees Daily Log')

        writer.close()
       
        return HttpResponse
    else:
        return JsonResponse({'result':'success'})

@csrf_exempt
def download_excel_data(request,id):
    #print('I am id'+id)
    filter = FilterQuery.objects.get(id=id)
    data = createReportData(filter.user.id,filter.date1,filter.date2,filter.log_type,filter.task_type)
    #print(data)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Log Data') # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id','Username', 'Date','Task Type', 'Task Name','Billable','Details','Hour' ]

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
            ws.write(i+1, j, row[col])

    wb.save(response)

    return response

@csrf_exempt
def hourApproval(request):
    if request.method == 'POST':
        month = request.POST.get('month')
        check = LogApproval.objects.filter(user=request.user,month=month)
        print(check)
        if not check:
            LogApproval(user=request.user,month=month,request=True,status=False).save()
            return JsonResponse({'result':'success'})
        else:
            return JsonResponse({'result':'Already requested for selected month!'})
            