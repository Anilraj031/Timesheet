from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse,HttpResponse
from .models import LoggedUser,Company,Employees,userDetails
from Manager.models import InitialPassword,Teams,TeamLeads,TeamUsers
import re
from django.contrib.auth.hashers import check_password
from Attendance.models import LeaveType
from django.views.decorators.csrf import csrf_exempt
from .forms import loginForm
from django.db.models import Q
from Manager.views import checkTeams
import random
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.


#manoj
def VerifySignupOTP(request):
    if request.method == "POST":
        userotp = request.POST.get('otp')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            form = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password1)
            form.save()
            #print("OTP: ", userotp)
            return HttpResponse('Hello')  # Replace JsonResponse with HttpResponse
        else:
            return HttpResponse(status=400)  # Return an appropriate response if passwords do not match
    return HttpResponse(status=400)  # Return an appropriate response for other request methods


def sign_up(request):
    form = UserCreationForm()
    if request.method == "POST":
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        form = UserCreationForm(request.POST)
        if form.is_valid():
            otp = random.randint(1000, 9999)
            send_mail("Signup OTP Email", f"Verify Your Mail by the OTP: {otp}", settings.EMAIL_HOST_USER, [email], fail_silently=True)
            messages.success(request, 'User saved successfully')
            return render(request, 'Authentication/VerifySignup.html', {'otp': otp, 'first_name': first_name, 'last_name': last_name, 'email': email, 'username': username, 'password1': password1, 'password2': password2})        
        else:
            print("Form Error: ", form.errors)
            messages.error(request, form.errors)
        context = {'form': form}
        return render(request, 'Authentication/register.html', context)
    return render(request, 'Authentication/register.html', {'form': form})

@csrf_exempt
def VerifyLoginOTP(request):
    if request.method == "POST":
        userotp = request.POST.get('otp')
        uname = request.POST.get('username')
        upass = request.POST.get('password')
        email = request.POST.get('email') 
        user = authenticate(username=uname, password=upass, email=email)
        if user is not None:
            login(request, user)
            createSession(request)
            device = request.META['HTTP_USER_AGENT']
            LoggedUser(user=request.user,device=device).save()
            #print("Login Done")
            #print("OTP: ", userotp)
        return JsonResponse({'data': 'Hello'}, status=200)
        
def login_n(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            uname = request.POST.get('username')
            upass = request.POST.get('password')
            email = request.POST.get('email') 
            user = authenticate(username=uname, password=upass)
            print(user)
            if user is not None:
                user_Details= userDetails.objects.get(user=user)
                #print(user_Details.is_mfa)
                if user_Details.is_mfa:
                    email = User.objects.get(username=uname).email
                    otp = random.randint(1000, 9999)
                    send_mail("Login OTP Email: ", f"Verify Your Mail by the OTP: {otp}", settings.EMAIL_HOST_USER, [email], fail_silently=True)
                    return render(request, 'Authentication/VerifyLogin.html', {'otp': otp, 'username': uname, 'password': upass})
                else:
                    login(request, user)
                    createSession(request)
                    device = request.META['HTTP_USER_AGENT']
                    LoggedUser(user=request.user,device=device).save()
                    return HttpResponseRedirect(reverse('home'))
            else:
                fm = {
                    'username': request.POST.get('username'),
                    'password': request.POST.get('password'),
                    'error': True
                }
                context = {
                    "forms": fm
                }
                return render(request,'Authentication/login.html',context)
        else:
            """
            checkPassword = InitialPassword.objects.get(user=request.user.id)
            if checkPassword.first_changed == False:
                return HttpResponseRedirect(reverse('newPassword'))
            else:
                return HttpResponseRedirect(reverse('home'))
            """
            return render(request, 'Authentication/login.html')


def addown(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        email=request.POST.get('email')
        get_company = request.POST.get('company')  # Retrieve the 'company' value from the form
        company_id=Company.objects.get(name=get_company)

        if form.is_valid():
            user=form.save()  # Save the user object to the database
            if user is not None:
                User.objects.filter(username=user).update(email=email) 
                newuser=User.objects.get(username=user)
                Employees(company=company_id, user=newuser).save()
                userDetails(user=user).save()

            messages.success(request, 'Sign up successful!')
            return HttpResponseRedirect(reverse('login'))
    else:
        context = {
            'form': form,
        }
        return render(request, 'Authentication/addown.html', context)


"""
def sign_up(request):
    if request.method == "POST":
        fm=UserCreationForm(request.POST)
        if fm.is_valid:
            fm.save()
        else:
            fm = UserCreationForm()
            messages.success(request, 'Somethings Wrong! Please try again with different value')
            
    else:
        fm = UserCreationForm()
    return render(request, 'Authentication/register.html', {'form':fm})


def login_n(request):
    if not request.user.is_authenticated :
        if request.method == 'POST':
            uname = request.POST.get('username')
            upass = request.POST.get('password')
            user = authenticate(username=uname, password=upass)
            #print(user)
            if user is not None:
                login(request,user)
                device = request.META['HTTP_USER_AGENT']
                LoggedUser(user=request.user,device=device).save()
                #print(request.user.id)
                
                if request.user.is_authenticated:
                    createSession(request)
                    checkPassword = InitialPassword.objects.get(user=request.user.id)
                    if checkPassword.first_changed == False:
                        return HttpResponseRedirect(reverse('newPassword'))
                    else:
                        return HttpResponseRedirect(reverse('home'))
            fm={
                'username':request.POST.get('username'),
                'password':request.POST.get('password'),
                'error':True
            }
            
        else:
            fm={
                
            }
            
        context = {
            "forms":fm
        }
        return render(request, 'Authentication/login.html', context)
    else:
        checkPassword = InitialPassword.objects.get(user=request.user.id)
        if checkPassword.first_changed == False:
            return HttpResponseRedirect(reverse('newPassword'))
        else:
            return HttpResponseRedirect(reverse('home'))
"""
def logout_n(request):
    device = request.META['HTTP_USER_AGENT']
    LoggedUser.objects.filter(user=request.user,device=device).delete()
    logout(request)
    return HttpResponseRedirect('login')

def getUser(request):
    if request.user.is_authenticated :
        username = str(request.user)
        return JsonResponse({'user':username})
    else:
        return HttpResponseRedirect('login')

def changePassword(request):
    return render(request, "Authentication/newPassword.html")

def updatePassword(request):
    if request.method == 'POST':
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        check = checkPassword(request,pass2)
        #print()
        
        if(pass1 != pass2 ):
            return JsonResponse({'result':"Password didn't matched!"})
        elif(check != 'Success' ):
            return JsonResponse({'result':check})
        else:
            usr = User.objects.get(username=request.user.username)
            usr.set_password(pass1)
            usr.save()
            InitialPassword.objects.filter(user_id=request.user.id).update(first_changed=True)
            return JsonResponse({'result':"Success"})
            #return HttpResponseRedirect(reverse('home'))

def resetPassword(request):
    return render(request, "Authentication/ResetPassword.html")


def checkPassword(request,password):
    password = password
    flag = ''
    currentpassword = request.user.password
    matchcheck= check_password(password, currentpassword)
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
        elif matchcheck:
            flag = 'Please enter new password!'
            break
        else:
            flag = 'Success'
            break
    return flag


def userSetting(request):
    ltypes = LeaveType.objects.all()
    team = Teams.objects.all()
    return render(request,'Authentication/usersettings.html',{'ltypes':ltypes,'teams':team})

def createSession(request):
    companyid = Employees.objects.get(user=request.user)
    #print(companyid.company.name)
    request.session['company'] =companyid.company.name
    request.session['comp'] = companyid.company.id
    #request.session['id'] = random.randint(1000, 9999)
    
    return True
@csrf_exempt
def activateUser(request):
    id=request.POST.get('userid')
    action = request.POST.get('action')
    if action=="true":
        User.objects.filter(id=id).update(is_active=True)
        return JsonResponse({'result':"Success"})
    else:
        User.objects.filter(id=id).update(is_active=False)
        return JsonResponse({'result':"Success"})


@csrf_exempt
def adminUser(request):
    id=request.POST.get('userid')
    action = request.POST.get('action')
    if action=="true":
        User.objects.filter(id=id).update(is_superuser=True)
        return JsonResponse({'result':"Success"})
    else:
        User.objects.filter(id=id).update(is_superuser=False)
        return JsonResponse({'result':"Success"})
    
def getTeams(request,teamid):
    team = Teams.objects.get(id=teamid)
    members = TeamUsers.objects.filter(team =teamid)
    manager = TeamLeads.objects.filter(team =teamid)
    #print(manager[0].lead)
    #print()
    return render(request,'Authentication/team.html',{'teams':team,'members':members,'manager':manager})

@csrf_exempt
def searchUser(request):
    user_name = request.POST.get('name')
    #print(user_name)
    allusers = checkTeams(request)
    users = User.objects.filter(~Q(id=request.user.id),username__startswith=user_name,pk__in=allusers[0]).values()
    return JsonResponse({'result':list(users)})

@csrf_exempt
def addToTeams(request):
    userList = request.POST.getlist('userlist[]')
    managerList = request.POST.getlist('managerlist[]')
    id = userList[0]
    #print(userList)
    userList.remove(id)
    team = Teams.objects.get(id=id)
    for u in userList:
        user = User.objects.get(username=u)
        checkUser = TeamUsers.objects.filter(team=team,user=user)
        
        if checkUser.exists() == False:
            tuser = TeamUsers(team=team,user=user)
            tuser.save()
    #add manager
    for m in managerList:
        muser = User.objects.get(username=m)
        checkManager = TeamLeads.objects.filter(team=team,lead=muser)
        if checkManager.exists() == False:
            TeamLeads(team=team,lead=muser).save()

    return JsonResponse({'result':'success'})

@csrf_exempt
def removeFromTeam(request):
    teamId = request.POST.get('team')
    userId = request.POST.get('user')
    type = request.POST.get('type')

    team = Teams.objects.get(id=teamId)
    user = User.objects.get(id=userId)
    if type=='manager':
        TeamLeads.objects.filter(team=team,lead=user).delete() 
    else:
        TeamUsers.objects.filter(team=team,user=user).delete()
    
    return JsonResponse({'result':"success"})


