from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/host/', views.register_host, name='register_host'),
    path('register/voter/', views.register_voter, name='register_voter'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    path('host/dashboard/', views.host_dashboard, name='host_dashboard'),
path('voter/dashboard/', views.voter_dashboard, name='voter_dashboard'),

path('approve-users/', views.approve_users, name='approve_users'),
path('approve/<int:user_id>/', views.approve_user, name='approve_user'),
path('reject/<int:user_id>/', views.reject_user, name='reject_user'),

path('host/approve-voters/', views.host_approve_voters, name='host_approve_voters'),
path('host/approve/<int:user_id>/', views.approve_voter, name='approve_voter'),

path('about/', views.about, name='about'),
path('contact/', views.contact, name='contact'),
path('host/reject-voter/<int:user_id>/', views.reject_voter, name='reject_voter'),

]