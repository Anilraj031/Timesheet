from django.shortcuts import render
from django.shortcuts import redirect
from . models import Ticket,ticketDetails
from Attendance.models import User
from Customer.models import employee
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Manager.views import checkTeams
from Authentication.models import Company,Employees
import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Create your views here.
# function based views
@login_required
def index(request):
    users = checkTeams(request)
    comp = request.session['comp']
    #print(users)
    allusers =User.objects.filter(pk__in=users[0]).values('id','username')
    #print(allusers)
    ticket = Ticket.objects.filter(company__id=comp)
    mytickets = Ticket.objects.filter(assigned_to= request.user)
    customer = employee.objects.all().values()
    #print(customer)
    dic = {
        'ticket':ticket,
        'users':list(allusers),
        'customer':list(customer),
        'mytickets':mytickets
        }
    return render(request, 'Issues/allIssues.html', dic)

def getIssue(request,issueid):
    issue = Ticket.objects.get(id=issueid)
    #print(datetime.date.today())
    issueComments = ticketDetails.objects.filter(ticket_id = issueid)
    #allusers =User.objects.all().values('id','username')
    allusers1 = checkTeams(request)
    allusers =User.objects.values('id','username').filter(pk__in=allusers1[0] )
    customer = employee.objects.all().values()

    #print(issueComments)
    return render(request, 'Issues/details.html',{'issue':issue,'users':allusers,'customer':customer,'comments':issueComments})

def ADD(request):
    if request.method == "POST":
        ticketName = request.POST.get('ticketName')
        ticketType = request.POST.get('ticketType')
        shortDesc = request.POST.get('shortDesc')
        dateOpened = request.POST.get('dateOpened')
        affUser = request.POST.get('affUser')
        priority = request.POST.get('priority')
        state = request.POST.get('state')
        assGroup = request.POST.get('assGroup')
        assTo = request.POST.get('assTo')
        email = request.POST.get('email')
        comments = request.POST.get('comments')
        comp = Company.objects.get(pk=request.session['comp'])

        tickets = Ticket(
            ticket_name = ticketName  ,
            ticket_type= ticketType,
            short_desc= shortDesc,
            open_date= dateOpened,
            affected_user= employee.objects.get(id=affUser),
            priority= priority,
            state= state,
            assigned_grp= assGroup,
            assigned_to= User.objects.get(id=assTo),
            email= email,
            comments=comments,
            company = comp
        )
        tickets.save()
        return redirect('index')
    return render(request, 'allIssues.html')


def EDIT(request):
    ticket = Ticket.objects.all()
    
    context  = {
        'ticket':ticket,
    }
    return redirect(request, 'allIssues.html',context)


def Update(request,id):
    if request.method == "POST":
        ticketName = request.POST.get('ticketName')
        ticketType = request.POST.get('ticketType')
        shortDesc = request.POST.get('shortDesc')
        dateOpened = request.POST.get('dateOpened')
        affUser = request.POST.get('affUser')
        priority = request.POST.get('priority')
        state = request.POST.get('state')
        assGroup = request.POST.get('assGroup')
        assTo = request.POST.get('assTo')
        email = request.POST.get('email')
        comments = request.POST.get('comments')
        comp = Company.objects.get(pk=request.session['comp'])

    #tickets = 
    Ticket.objects.filter(id=id).update(
            ticket_name = ticketName  ,
            ticket_type= ticketType,
            short_desc= shortDesc,
            last_updated= datetime.date.today(),
            affected_user= employee.objects.get(id=affUser),
            priority= priority,
            state = state,
            assigned_to= User.objects.get(id=assTo),
            comments=comments
    )
    
    #tickets.save()
    return redirect('index')
    return redirect(request,'allIssues.html')


def Done(request):
    if request.method == "POST":
        return redirect(request, 'allIssues.html')


def DELETE(request,id):
    ticket=Ticket.objects.filter(id = id).delete()
    context ={
         'ticket':ticket,
    }
    return redirect('index')
    return redirect(request,'allIssues.html', context)


def done(request):
    return redirect(request, 'allIssues.html' )

@csrf_exempt
def updateStatus(request):
    status=request.POST['status']
    id=request.POST['id']
    print(status)
    if status == 'new':
        Ticket.objects.filter(id=id).update(state='New')
    elif status == 'inprogress':
        Ticket.objects.filter(id=id).update(state='InProgress')
    elif status == 'hold':
        Ticket.objects.filter(id=id).update(state='Hold')
    elif status == 'complete':
        Ticket.objects.filter(id=id).update(state='Completed')
    else:
        Ticket.objects.filter(id=id).update(state='Canceled')
    return JsonResponse({'result':"success"})

@csrf_exempt
def addComments(request):
    if request.method == "POST":
        id = request.POST.get('id')
        #print(id)
        ticket = Ticket.objects.get(id=id)
        comments = request.POST.get('newcomment')

        details = ticketDetails(ticket = ticket, comments = comments,user=request.user)
        details.save()
        
        getComment = ticketDetails.objects.last()
        return JsonResponse({'date':getComment.date.strftime("%B %d, %Y %I:%M %p"),'comment':getComment.comments,'user':getComment.user.username})

def getMyTask(request):
    if request.method == 'GET':
        issues = Ticket.objects.filter(Q(state='New')|Q(state='Pending'),assigned_to = request.user).values()
        return JsonResponse({'tasks':list(issues)})