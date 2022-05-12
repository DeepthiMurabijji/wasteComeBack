from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from trash.models import *

# Create your views here.


def home(request):
    return render(request, 'home.html')


def register(request):

    areas = Areas.objects.all()
    context = {'areas': areas}

    return render(request, 'register.html', context)


def register_save(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        areas = Areas.objects.get(area_name = request.POST.get('area')) 

        if password == password1:
            user = User.objects.create_user(username = username, email = email)
            user.set_password(password)
            user.save()

            collector = Collector()

            collector.user = user
            collector.area = areas
            collector.is_admin = False
            collector.area_status = False
            collector.is_real = False
            collector.save()


    return redirect('/')

def loginn(request):
    return render(request, 'login.html')


def login_output(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        
        except:
            return HttpResponse("Not right")

        collector = Collector.objects.get(user=user)

        authenUser = authenticate(username = username, password = password)

        if authenUser is not None:

            login(request, authenUser)
            # return HttpResponse("Correcty")

            if collector.is_admin == True:
                return render(request, 'admin-panel.html')
            else:
                if collector.is_real == True:
                    return render(request, 'member-panel.html')
                else:
                    return HttpResponse("Get the fuck out of here")
        else: 
            return HttpResponse("Wrong Credentials")

    return redirect('/')


def member_job_status(request):

    if request.method == 'POST':

        username = request.user.username
        job_status = request.POST.get('job')

        if job_status == "Done":
            job_status = True
        else:
            job_status = False

        user = User.objects.get(username=username)
        Collector.objects.filter(user = user).update(area_status = job_status)

    return HttpResponse("You submitted!")


def admin_permissions(request):

    collector = Collector.objects.all()

    context = {

        'collectors': collector

    }

    return render(request, 'admin-permissions.html', context)

def admin_permissions_save(request, username):

    if request.method == 'POST':

        adminChoice = request.POST.get('admin')

        user = User.objects.get(username = username)

        print(user.username)

        if adminChoice == "True":
            adminChoice = True
        else: 
            adminChoice = False

        Collector.objects.filter(user = user).update(is_admin = adminChoice)

    return redirect('admin-permissions')

def collector_authentic_permissions(request, username):

    if request.method == 'POST':

        isRealChoice = request.POST.get('real')

        if isRealChoice == "True":
            isRealChoice = True
        else: 
            isRealChoice = False

        user = User.objects.get(username = username)
        Collector.objects.filter(user=user).update(is_real = isRealChoice)

    return redirect('admin-permissions')


def logoutt(request):
    logout(request)
    return redirect('/')