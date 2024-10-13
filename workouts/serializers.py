from rest_framework import serializers
from .models import Exercise, RecommendedExercise

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'title', 'body_part', 'equipment', 'description']


class RecommendedExerciseSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True)

    class Meta:
        model = RecommendedExercise
        fields = ['id', 'exercises', 'muscle_group', 'user']  # Update fields

    def create(self, validated_data):
        exercises_data = validated_data.pop('exercises')
        recommended_exercise = RecommendedExercise.objects.create(**validated_data)

        for exercise_data in exercises_data:
            exercise, created = Exercise.objects.get_or_create(
                id=exercise_data.get('id'),
                defaults=exercise_data
            )
            recommended_exercise.exercises.add(exercise)

        return recommended_exercise