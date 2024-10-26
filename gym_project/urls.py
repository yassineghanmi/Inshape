"""
URL configuration for gym_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from gym_project.views import registration_view, profile
from gym_project import views

urlpatterns = [
    path('', views.index, name='index'),
    path('class-details/', views.classes, name='class_details'),
    path('services/', views.services, name='services'),
    path('team/', views.team, name='team'),
    path('class-timetable/', views.class_timetable, name='class_timetable'),
    path('bmi-calculator/', views.bmi_calculator, name='bmi_calculator'),
    path('gallery/', views.gallery, name='gallery'),
    path('blog/', views.blog, name='blog'),
    path('404/', views.error_404, name='error_404'),
    path('contact/', views.contact, name='contact'),
    path('about-us/', views.about_us, name='about_us'),
    path('admin/', admin.site.urls),
    path('api/exercises/', include('workouts.urls')),
     # Authentication URLs (customize password reset email here)
    path(
        'accounts/password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            extra_context={'protocol': 'http', 'domain': '127.0.0.1:8000'}
        ),
        name='password_reset'
    ),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', registration_view, name='register'),
    path("accounts/profile/", profile, name="profile"),

   path('getResponse', views.getResponse, name='getResponse'),
   
    
]
