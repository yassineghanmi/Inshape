from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_exercise, name='generate_exercise'),
    path('save/', views.save_exercise_recommendation, name='save_exercise_recommendation'),
    path('recommendations/<str:user>/', views.view_recommendations, name='view_recommendations'),
    path('delete/<int:recommendation_id>/', views.delete_recommendation, name='delete_recommendation'),
]
