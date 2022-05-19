
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from trash.models import *
from django.contrib import messages 
from django.urls import reverse
# Create your views here.


def home(request):
    return render(request, 'home.html')


def register(request):

    areas = Areas.objects.all()
    context = {'areas': areas}

    return render(request, 'register.html', context)


def register_save(request):

    areas = Areas.objects.all()

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        areas = Areas.objects.get(area_name = request.POST.get('area')) 

        if password == password1:

            if (User.objects.filter(username=username).exists()):
                print("username already exists")
                areas = Areas.objects.all()

                context = {
                            'areas': areas,
                            'name': 'User already exists try another',
                }
                return render(request, 'register.html',context)  
            else:
                # user = User.objects.create_user(username = username,email = email)

                if (User.objects.filter(email = email).exists()):
                    print("email already exists")
                    areas = Areas.objects.all()

                    context = {
                        'areas': areas,
                        'email': 'Email already exists try another',
                    }
                    return render(request, 'register.html', context)  
                else:
                    user = User.objects.create_user(username = username,email = email)

        
            user.set_password(password)
            user.save()

            collector = Collector()

            collector.user = user
            collector.area = areas
            collector.is_admin = False
            collector.area_status = False
            collector.is_real = False
            collector.save()
        else:
            areas = Areas.objects.all()

            context = {
                 'areas': areas,
                 'message': 'password does not match',
            }
            return render(request, 'register.html',context) 
        return render(request, 'waiting.html')
    else:
        return render(request, 'register.html')

registerKey = True

def loginn(request):

    # registerKey = True
    global registerKey
    registerKey = True

    context ={
        'registerKey': registerKey
    }

    return render(request, 'login.html', context)


def login_output(request):
    global registerKey
    registerKey = True

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            print(user)
        except:

            messages.success(request,"PLEASE ENTER CORRECT USERNAME")
           
            return render(request, 'login.html',{'message':'PLEASE ENTER CORRECT USERNAME'})

        collector = Collector.objects.get(user=user)
        house = Houses.objects.filter(area=collector.area)
        print("here is the house",house)


        authenUser = authenticate(username = username, password = password)
        print(authenUser)

        if authenUser is not None:

            login(request, authenUser)
            # return HttpResponse("Correcty")
           

            if collector.is_admin == True:
                adminKey = True

                context ={
                    'adminKey': adminKey,
                    'collector': collector,
                }
                # return render(request, 'admin-panel.html',context)
                # print("Collector Here",type(collector),type(collector.user.username))
                return redirect('admin-panel',collector)  
            else:
                if collector.is_real == True:
                    adminKey = True
                    context ={
                         'adminKey': adminKey,
                         'collector': collector,
                         'house': house,
                         }
                    return render(request, 'member-panel.html', context)
                else:
                    return render(request, 'login.html',{'message':'YOUR ACCOUNT IS NOT ACTIVATED !'})
        else: 
            messages.success(request,("There was a problem login "))
            return render(request, 'login.html',{'message':'PLEASE LOGIN WITH A CORRECT PASSWORD'})
    
    else:
        messages.success(request,('There was a problem login'))
        return render(request, 'login.html', {'registerKey': registerKey})

def admin_panel(request, collector):
    print("I am here at Panel",collector)
    adminKey = True
    context ={
        'adminKey': adminKey,
        'collector': collector,
    }
    return render(request, 'admin-panel.html', context)

def admin_profile(request,username):
    user = User.objects.get(username=username)
    profile = Collector.objects.get(user=user)
    adminKey = True
    context = {
        'profile': profile,
        'adminKey': adminKey,
    }
    return render(request, 'adminprofile.html', context)

def member_job_status(request):
    global findKey
    findKey = True

    if request.method == 'POST':

        global job_status
        username = request.user.username
        job_status = request.POST.get('job')

        if job_status == "Done":
            job_status = True
        else:
            job_status = False
    
        user = User.objects.get(username=username)
        Collector.objects.filter(user = user).update(area_status = job_status)
        context = {
                'job_status': job_status,
                'findKey': findKey,
            }


    return render(request, 'thank.html', context)


def admin_permissions(request):

    collector = Collector.objects.all()
    adminKey = True
    findKey = True

    context = {

        'collectors': collector,
         'adminKey': adminKey,
         'findKey': findKey,
         

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

def admin_area(request):

    adminKey = True
    areas = Areas.objects.all()

    if request.method == 'POST':

        area_name = request.POST.get('areaname')
        house_name = request.POST.get('housename')
        address = request.POST.get('address')
        house = Houses()

        if (Areas.objects.filter(area_name=area_name).exists()):
            print ('Areas already exists')
            house.area = Areas.objects.get(area_name=area_name)
            house.house_name = house_name
            house.house_address = address
            house.save()
        else:
            print("areas not exists")
            area = Areas()
            area.area_name = area_name
            area.save()
            # areas = Areas.objects.get(area_name = request.POST.get('area'))  
            print('Area is added now !')
            house.area = area
            house.house_name = house_name
            house.house_address = address
            house.save()
        context ={
            'adminKey' : adminKey,
            'areas': areas,
            'success' : "your response has been recorded",
        }
        return render(request, 'adminarea.html', context)
    else:
        context = {
            'adminKey' : adminKey,
            'areas': areas,
        }

        return render(request, 'adminarea.html', context)


def admin_search(request):
    adminKey = True
    if request.method == 'POST':

        findout = request.POST['username']
        #print("search: ",findout)
        #user = User.objects.filter(username = findout)
       # search = Collector.objects.filter(user)
        print('________________________________________________________')
       # print("search got: ",search)
        # print(user)
        user = User.objects.filter(username__contains = findout)
        # search = Collector.objects.prefetch_related('user').filter(user=user)
        search = Collector.objects.filter(user_id__in = user)
        context = {
            'search' : search,
            'adminKey' : adminKey,
        }

        return render(request, 'admin-search.html',context)
    else:
        return HttpResponse("not found", status=404)

def logoutt(request):
    logout(request)
    return render(request,'home.html')