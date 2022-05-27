from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('loginn/', views.loginn, name="loginn"),
    path('login_req/',views.login_req, name="login-req"),
    path('logoutt/', views.logoutt, name="logoutt"),
    path('login-output/', views.login_output, name="login-output"),
    path('register/', views.register, name="register"),
    path('register-save/', views.register_save, name="register-save"),
    path('memeber-job-status/', views.member_job_status, name="memeber-job-status"),
    path('admin-panel/', views.admin_panel, name="admin-panel"),
    path('admin-permissions/', views.admin_permissions, name="admin-permissions"),
    path('admin-permissions-save/<str:username>/', views.admin_permissions_save, name="admin-permissions-save"),
    path('collector-authentic-permissions/<str:username>/', views.collector_authentic_permissions, name="collector-authentic-permissions"),
    path('admin-profile/', views.admin_profile, name="admin-profile"),
    path('admin-area/', views.admin_area, name="admin-area"),
    path('admin-search/', views.admin_search, name="admin-search"),
    path('viewarea/', views.viewarea, name="viewarea"),
    path('csvfile/',views.create_csv_file, name="csvfile"),
    path('reset/',views.reset, name="reset"),
    
]
