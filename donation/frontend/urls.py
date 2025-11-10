from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('signup/', views.signup_step1, name='signup_step1'),
    path('signup/donor/', views.signup_donor, name='signup_donor'),
    path('signup/ngo/', views.signup_ngo, name='signup_ngo'),
    path('signup/recipient/', views.signup_recipient, name='signup_recipient'),
    path('signup/success/', views.signup_success, name='signup_success'),
    path('donor/', views.donor_dashboard, name='donor'),
    path('recipient/', views.recipient_dashboard, name='recipient'),
    path('ngo/', views.ngo_dashboard, name='ngo'),
    path('donations/', donations_list_create, name='donations'),
]