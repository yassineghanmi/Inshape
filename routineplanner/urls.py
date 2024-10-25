# routineplanner/urls.py
from django.urls import path
from . import views
from .views import workout_view, save_routine ,success_view 

urlpatterns = [
    path('workout/', workout_view, name='workout_view'),
    path('save-routine/', save_routine, name='save_routine'),  # New path for saving the routine
    path('success/', success_view, name='success_url'),  # New path for success URL


]
