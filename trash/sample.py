# from django.http import HttpResponse
# from django.shortcuts import render, redirect
# from trash.models import *
# from django.contrib.auth import authenticate, login, logout

# global regkey 
# regkey = True 

# global logkey
# logkey = True

# def home(request):
#     render(request, 'home.html')


# def register_save(request):

#     areas = Areas.objects.all()
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         password1 = request.POST.get('password1')
#         areas = Areas.objects.get(area_name = request.POST.get('area'))

#         if password == password1:
#             if (User.objects.filter(username=username).exists()):
               
#                context = {
#                    'areas' : areas,
#                    'name':'User already exists',
#                }
#                return render(request, 'register.html', context)
#             else:
#                 if (User.objects.filter(email=email).exists()):

#                     context = {
#                         'areas': areas,
#                         'email': 'Email already exists try another',
#                     }
#                 else:
#                     user = User.objects.create_user(username= username,email = email)
#             user.set_password(password)
#             user.save()

#             collector = Collector()
#             collector.user = user
#             collector.area = areas
#             collector.is_admin = False
#             collector.area_status = False
#             collector.is_real = False
#             collector .save()
#             return render(request, 'waiting.html')
#         else :
#             context = {
#                 'areas':areas,
#                 'password':'password did not match',
#             }
#             return render(request, 'register.html', context)
#     else :
#         return render(request, 'register.html')

# def login_output(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         try:
#             user = User.objects.get(username = username)
#         except:
#             return render(request, 'login.html',{'message':'PLEASE ENTER CORRECT USERNAME'})
#         collector = Collector.objects.get(user = user)
#         house = Houses.objects.filter(area=collector.area)
#         authenUser = authenticate(username= username, password= password) 
#         if authenUser is not None:
#             login(request, authenUser)
#             if (collector.is_admin == True and collector.is_real == True):
#                 context = {

#                 }
#                 return redirect('admin-panel')   
#             elif collector.is_real == True:
                
#                 context = {

#                 }
#                 return render(request, 'member-panel.html', context)
#             else:
#                 return render(request, 'login.html',{'message':'YOUR ACCOUNT IS NOT ACTIVATED !'})
                
