# workouts/views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Exercise
from .serializers import ExerciseSerializer
from ml_models.exercise_recommender import get_exercise_recommendation  # import your ML model from wherever it's stored
from rest_framework import generics
from .models import RecommendedExercise
from .serializers import RecommendedExerciseSerializer


import math

class ExerciseRecommendationView(APIView):
    def post(self, request):
        muscle_group = request.data.get('muscle_group')
        level = request.data.get('level')
        total_exercises = request.data.get('total_exercises', 8)

        try:
            recommendations = get_exercise_recommendation(muscle_group, level, total_exercises)
            response_data = []

            for title, equipment, body_part, description in recommendations:
                # Check for nan values and replace them with a string "nan" or None
                if isinstance(description, float) and math.isnan(description):
                    description = "Empty"  # or description = None

                response_data.append({
                    "title": title,
                    "body_part": body_part,
                    "equipment": equipment,
                    "description": description
                })

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# List all recommended exercises and create new recommendation
class RecommendedExerciseListCreateView(generics.ListCreateAPIView):
    queryset = RecommendedExercise.objects.all()
    serializer_class = RecommendedExerciseSerializer

    def perform_create(self, serializer):
        # Customize creation logic to save muscle_group
        muscle_group = self.request.data.get('muscle_group')
        serializer.save(muscle_group=muscle_group)


# Retrieve, update, or delete a specific recommended exercise
class RecommendedExerciseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecommendedExercise.objects.all()
    serializer_class = RecommendedExerciseSerializer

# Create a view to retrieve recommended exercises by user and muscle group
class RecommendedExerciseByUserAndMuscleGroupView(generics.ListAPIView):
    serializer_class = RecommendedExerciseSerializer

    def get_queryset(self):
        user = self.request.query_params.get('user')
        muscle_group = self.request.query_params.get('muscle_group')

        # Filter based on user and muscle group
        queryset = RecommendedExercise.objects.all()
        if user:
            queryset = queryset.filter(user=user)
        if muscle_group:
            queryset = queryset.filter(muscle_group=muscle_group)

        return queryset