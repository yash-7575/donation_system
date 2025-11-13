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

    # Dashboards
    path('donor/', views.donor_dashboard, name='donor'),
    path('donor/update/<int:donation_id>/', views.update_donation, name='update_donation'),
    path('donor/delete/<int:donation_id>/', views.delete_donation, name='delete_donation'),
    path('recipient/', views.recipient_dashboard, name='recipient'),
    path('ngo/', views.ngo_dashboard, name='ngo'),
    
    # API endpoints for NGO dashboard
    path('api/donors/', views.donors_api, name='donors_api'),
    path('api/recipients/', views.recipients_api, name='recipients_api'),
]