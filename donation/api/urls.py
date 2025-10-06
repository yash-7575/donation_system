from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health),
    path('demo/superadmin/', views.superadmin_demo),
    path('donors/', views.donors_list_create),
    path('recipients/', views.recipients_list_create),
    path('ngos/', views.ngos_list_create),
    path('donations/', views.donations_list_create),
    path('donations/match/', views.match_donation),
]


