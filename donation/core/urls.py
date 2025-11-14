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
    path('recipient/', views.recipient_dashboard, name='recipient'),
    path('ngo/', views.ngo_dashboard, name='ngo'),
    
    path('donor/update/<int:donation_id>/', views.update_donation, name='update_donation'),
    path('donor/delete/<int:donation_id>/', views.delete_donation, name='delete_donation'),
    
    # Recipient request management
    path('recipient/update/<int:request_id>/', views.update_request, name='update_request'),
    path('recipient/delete/<int:request_id>/', views.delete_request, name='delete_request'),
    
    # Feedback URLs
    path('donor/feedback/', views.donor_feedback, name='donor_feedback'),
    path('recipient/feedback/', views.recipient_feedback, name='recipient_feedback'),
    path('ngo/feedback/', views.ngo_feedback, name='ngo_feedback'),
    
    # Recipient feedback management
    path('recipient/feedback/edit/<int:id>/', views.edit_feedback, name='edit_feedback'),
    path('recipient/feedback/delete/<int:id>/', views.delete_feedback, name='delete_feedback'),
    
    # API endpoints for NGO dashboard
    path('api/donors/', views.donors_api, name='donors_api'),
    path('api/recipients/', views.recipients_api, name='recipients_api'),
    
    # API endpoints for DBMS demo
    path('api/dbms/inner/', views.dbms_demo_inner_join, name='dbms_demo_inner_join'),
    path('api/dbms/left/', views.dbms_demo_left_join, name='dbms_demo_left_join'),
    path('api/dbms/right/', views.dbms_demo_right_join, name='dbms_demo_right_join'),
    path('api/dbms/self/', views.dbms_demo_self_join, name='dbms_demo_self_join'),
    path('api/dbms/complex/', views.dbms_demo_complex_join, name='dbms_demo_complex_join'),
    path('api/dbms/full/', views.dbms_demo_full_join, name='dbms_demo_full_join'),
    path('api/dbms/request_full/', views.dbms_demo_request_full_join, name='dbms_demo_request_full_join'),
    
    # NGO action endpoints
    path('ngo/accept_donation/<int:donation_id>/', views.accept_donation, name='accept_donation'),
    path('ngo/decline_donation/<int:donation_id>/', views.decline_donation, name='decline_donation'),
    path('ngo/accept_request/<int:request_id>/', views.accept_request, name='accept_request'),
    path('ngo/decline_request/<int:request_id>/', views.decline_request, name='decline_request'),
    path('ngo/mark_delivered/<int:donation_id>/', views.mark_delivered, name='mark_delivered'),
    path('ngo/mark_fulfilled/<int:request_id>/', views.mark_fulfilled, name='mark_fulfilled'),
]