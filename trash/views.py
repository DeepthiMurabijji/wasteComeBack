from multiprocessing import context
from django.utils.functional import SimpleLazyObject
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from trash.models import *
from django.contrib import messages 
from django.urls import reverse
from django.template.loader import get_template

# Create your views here.


def home(request):
    context={}
    if request.user.is_authenticated:
        context={
            'username' : request.user.username
        }
     
    return render(request, 'home.html', context)


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

def login_req(request):
    print("Here1",request.method)
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            print(user)
        except:

            messages.success(request,"PLEASE ENTER CORRECT USERNAME")
           
            return render(request, 'login.html',{'message':'PLEASE ENTER CORRECT USERNAME'})

        userme = User.objects.get(username=username)
        #print(userme.password)
        authenUser = authenticate(request, username = username, password = password)
        #print(authenUser)

        if authenUser is not None:

            login(request, authenUser)
            return redirect('login-output')

    return render(request, 'login.html')

@login_required(login_url='login-req')
def login_output(request):
    global registerKey
    registerKey = True
    print("1",type(request.user),request.user.username,request.user.is_superuser)
    users = User.objects.all()
    if request.user in users:
        collector_ = Collector.objects.get(user=request.user)
        print ("what?" ,collector_)
    if request.user in users and collector_.is_admin == False:
        registerKey = False
        user = User.objects.get(username=request.user.username)
        collector = Collector.objects.get(user=user)
        house = Houses.objects.filter(area=collector.area) 
        context ={
                'adminKey': True,
                'collector': collector,
                'house': house,
                'user':user,
                'registerKey':registerKey,
                }
        return render(request, 'member-panel.html', context)
    elif request.user in users and collector_.is_admin == True:
        return redirect("admin-panel")
    elif request.method == 'POST':

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
                }
                # return render(request, 'admin-panel.html',context)
                # print("Collector Here",type(collector),type(collector.user.username))
                return redirect('admin-panel')  
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

@login_required(login_url='login-output')
def admin_panel(request):
    adminKey = True
    context ={
        'adminKey': adminKey,
        'collector': request.user.username,
    }
    return render(request, 'admin-panel.html', context)

@login_required(login_url='login-output')
def admin_profile(request):
    user = User.objects.get(username=request.user.username)
    profile = Collector.objects.get(user=user)
    adminKey = True
    context = {
        'profile': profile,
        'adminKey': adminKey,
    }
    return render(request, 'adminprofile.html', context)

@login_required(login_url='login-output')
def member_job_status(request):
    global findKey
    findKey = True

    if request.method == 'POST':

        username = request.user.username
        job_status = request.POST.get('job')

        if job_status == "Done":
            job_status = True
        elif job_status == "Not Done":
            job_status = False
        
            
            collector = Collector.objects.get(user=request.user)
            house = Houses.objects.filter(area=collector.area)
            context ={
                    'collector': collector,
                    'house': house,
                    'adminKey': True,
                    }
            return render(request, 'member-panel.html', context)
    
        user = User.objects.get(username=username)
        Collector.objects.filter(user = user).update(area_status = job_status)
        context = {
                'job_status': job_status,
                'findKey': findKey,
            }


    return render(request, 'thank.html', context)

@login_required(login_url='login-output')
def admin_permissions(request):

    #collector = Collector.objects.prefetch_related('area', 'user').all()
    #collector = Collector.objects.all()
    #area = Areas.objects.get(area_name = collector.area)
    #house = Houses.objects.filter(area = area)
   # print("admin_permissions houses: ",house)
    areas = Areas.objects.all()
    collectors = Collector.objects.prefetch_related('area', 'user').all()
    collector_houses = {}
    for collector in collectors.iterator():
            print(" .........entered if ............")
            print(collector.area.area_name)
            houses = Houses.objects.filter(area = collector.area.id)
            collector_houses[collector] = houses
            for house in houses.iterator():
                print("Name:", collector.user.username)
                print("houses: ",house.house_name)
                print("address: ",house.house_address)
                   
       

    print("collectors: ", collectors)

    adminKey = True
    findKey = True

    context = {

        'collectors': collectors,
         'adminKey': adminKey,
         'findKey': findKey,
         'houses': houses,
         'collector_houses' : collector_houses,
         

    }

    return render(request, 'admin-permissions.html', context)

@login_required(login_url='login-output')
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

@login_required(login_url='login-output')
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

@login_required(login_url='login-output')
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

@login_required(login_url='login-output')
def viewarea(request):
    adminKey = True

    area = Areas.objects.all()
    print("hi ther:", id)
    houses = Houses.objects.all()
    
    print("areas are: ", area)
    print("houses: ", houses)
    context = {
        'adminKey' : adminKey,
        'houses': houses,
        'areas': area,
    }
    return render(request, 'viewareas.html', context)

@login_required(login_url='login-output')
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
         # search = Collector.objects.prefetch_related('user').filter(user=user)
        # if (User.objects.filter(username__contains = findout)):
            # user = User.objects.filter(username__contains = findout)
            # search = Collector.objects.filter(user_id__in = user)
        # else:
        user = User.objects.filter(username__contains = findout)
        search = list(Collector.objects.filter(user_id__in = user))
        area = Areas.objects.filter(area_name__contains = findout)
        print("area: ",area)
        search += set(list(Collector.objects.filter(area_id__in= area)))
        search = list(search)
        print("this is the area: " ,search)

        collector_houses = {}
        for collector in search:
            houses =Houses.objects.filter(area_id = collector.area_id )
            collector_houses[collector] = houses
            
            print ('search is here:', search)
        context = {
            'search' : search,
            'adminKey' : adminKey,
            'collector_houses': collector_houses,
        }

        return render(request, 'admin-search.html',context)
    else:
        return HttpResponse("not found", status=404)

def logoutt(request):
    logout(request)
    #return render(request,'home.html')
    return redirect('home')