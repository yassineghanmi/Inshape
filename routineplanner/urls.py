# routineplanner/urls.py
from django.urls import path
from . import views
from .views import workout_view, save_routine ,success_view,RoutineDetailView,delete_routine,edit_routine

urlpatterns = [
    path('workout/', workout_view, name='workout_view'),
    path('save-routine/', save_routine, name='save_routine'),  # New path for saving the routine
    path('success/', success_view, name='success_url'),  # New path for success URL
    path('routine/<int:id>/', RoutineDetailView.as_view(), name='routine_detail'),
    path('routine/delete/<int:id>/', delete_routine, name='delete_routine'),
    path('routine/edit/<int:routine_id>/', edit_routine, name='edit_routine'),


]
