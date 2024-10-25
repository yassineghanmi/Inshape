# routineplanner/urls.py
from django.urls import path
from . import views
from .views import workout_view

urlpatterns = [
        path('workout/', workout_view, name='workout_view'),


]
