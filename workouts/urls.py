# workouts/urls.py

from django.urls import path
from .views import ExerciseRecommendationView, RecommendedExerciseDetailView, RecommendedExerciseByUserAndMuscleGroupView, RecommendedExerciseListCreateView

urlpatterns = [
    path('recommend/', ExerciseRecommendationView.as_view(), name='exercise_recommendation'),
    # List and Create Recommended Exercises
    path('recommended/', RecommendedExerciseListCreateView.as_view(), name='recommended_exercise_list_create'),
    # Retrieve, Update, and Delete a specific Recommended Exercise
    path('recommended/<int:pk>/', RecommendedExerciseDetailView.as_view(), name='recommended_exercise_detail'),
    path('recommended/filter', RecommendedExerciseByUserAndMuscleGroupView.as_view(), name='recommended_exercise_filter'),
]
