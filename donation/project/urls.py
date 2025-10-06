from django.contrib import admin
from django.urls import path, include
from frontend import views as frontend_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', frontend_views.home, name='home'),
    path('login/', frontend_views.login_page, name='login'),
    path('register/', frontend_views.register_page, name='register'),
    path('donor/', frontend_views.donor_dashboard, name='donor'),
    path('recipient/', frontend_views.recipient_dashboard, name='recipient'),
    path('ngo/', frontend_views.ngo_dashboard, name='ngo'),
]


