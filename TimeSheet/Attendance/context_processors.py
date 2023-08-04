from django.db.models import Q
from Manager.views import checkTeams
import datetime
from Attendance.models import Leave
from emp_worklog.models import LogApproval
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def getNewLeaves(request):
    if request.user.id:
        is_manager = checkTeams(request)
        if is_manager[1] == True:
            new_leaves = Leave.objects.filter(user__id__in=is_manager[0],approval = 2)
        else: 
            today = datetime.datetime.now()
            new_leaves = Leave.objects.filter(user=request.user,date_approved__gte=today.date())
            #print(today.date())
        #print(new_leaves)
        return {"manager":is_manager[1],'n_leaves':new_leaves}
    else:
        return {}


def getLogApproval(request):
    if request.user.id:
        is_manager = checkTeams(request)
        if is_manager[1] == True:
            l_approval = LogApproval.objects.filter(user__id__in=is_manager[0],request=True)
        else: 
            l_approval = LogApproval.objects.filter(user=request.user,status=True)
            #print(today.date())
        #print(new_leaves)
        return {'n_log_approval':l_approval}
    else:
        return {}