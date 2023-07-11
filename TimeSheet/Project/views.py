from django.shortcuts import render
from .models import Project,SubProject
from emp_worklog.models import worklog
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from decimal import Decimal

# Create your views here.
def projects(request):
    all = Project.objects.all()
    result ={
        'projects':all,
        'count':all.count()
    }
    return render(request,'projects/viewProjects.html',result)

def getProject(request,pid):
    project = Project.objects.get(id=pid)
    sproject1 = SubProject.objects.filter(project=pid)
    sproject = []
    for x in sproject1:
        sproject.append({
            'id':x.id,
            'project':x.project.name,
            'manager':x.project.manager.username,
            'name':x.name,
            'details':x.details,
            'assigned_to':x.assigned_to,
            'hours':x.hour,
            'hours_done':x.hours_done,
            'percent': round(Decimal((x.hours_done/x.hour)*100),2)
        })
    #print(sproject)
    data = {'project':project,'subtask':sproject}
    #for n in sproject:
    #    getTask = worklog.objects.filter(project_id=n.id)
    #    for k in getTask:
    #        data[n.name] = getTask
    #print(data)
    return render(request,'projects/project.html',data)

@csrf_exempt
def getSubDetails(request):
    id = request.POST['id']
    getTask = worklog.objects.filter(project_id=id)
    newdata = getNames(request,getTask)
   
    return JsonResponse({'result':newdata})

def getNames(request,result):
    if request.user.is_superuser:
        alldata =[]
        for x in result:
            alldata.append({
                'id':x.id,
                'user':x.User.username,
                'date':x.Date,
                'type':x.TaskType.TaskType,
                'details':x.Workdone,
                'hour':x.Hours
            })
    else:
        alldata =[]
        for x in result:
            alldata.append({
                'id':x.id,
                'user':x.User.username,
                'date':x.Date,
                'type':x.TaskType.TaskType,
                'details':x.Workdone,
                'hour':x.Hours
            })
    return alldata