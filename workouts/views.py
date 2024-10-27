# workouts/views.py

from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Exercise, RecommendedExercise
from .forms import RecommendationForm
from ml_models.exercise_recommender import get_exercise_recommendation

def generate_exercise(request):
    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            muscle_group = form.cleaned_data['muscle_group']
            level = form.cleaned_data['level']
            total_exercises = form.cleaned_data['total_exercises']
            user = form.cleaned_data['user']

            # Generate the recommendation using the ML model
            recommended_exercises_data = get_exercise_recommendation(muscle_group, level, total_exercises)

            # Show recommendations to the user
            return render(request, 'recommend_exercises.html', {
                'recommended_exercises': recommended_exercises_data,
                'user': user,
                'muscle_group': muscle_group
            })
    else:
        form = RecommendationForm()

    return render(request, 'generate_exercise.html', {'form': form})


def save_exercise_recommendation(request):
    if request.method == 'POST':
        muscle_group = request.POST.get('muscle_group')
        user = request.POST.get('user')
        exercises = request.POST.getlist('exercises[]')  # List of exercise titles from the form

        # Check if recommendation already exists for this user and muscle group
        recommendation, created = RecommendedExercise.objects.get_or_create(
            user=user,
            muscle_group=muscle_group
        )

        # Clear previous exercises if updating the recommendation
        if not created:
            recommendation.exercises.clear()

        # Add the new exercises to the recommendation
        for exercise_title in exercises:
            try:
                # Find the exercise by title, using case-insensitive matching and stripping whitespaces
                exercise = Exercise.objects.get(title__iexact=exercise_title.strip())
                recommendation.exercises.add(exercise)  # Add exercise to the ManyToMany field
            except Exercise.DoesNotExist:
                # If an exercise doesn't exist, create it dynamically (e.g., from the generated data)
                # Assuming the form or ML model provides the necessary fields:
                description = request.POST.get(f"description_{exercise_title}", "No description")
                body_part = request.POST.get(f"body_part_{exercise_title}", "Unknown body part")
                equipment = request.POST.get(f"equipment_{exercise_title}", "Unknown equipment")

                # Create the new exercise
                exercise = Exercise.objects.create(
                    title=exercise_title.strip(),
                    body_part=body_part,
                    equipment=equipment,
                    description=description
                )

                # Add the new exercise to the recommendation
                recommendation.exercises.add(exercise)

        recommendation.save()  # Save the recommendation after adding exercises

        return redirect('view_recommendations', user=user)

    return redirect('generate_exercise')

def view_recommendations(request, user):
    recommendations = RecommendedExercise.objects.filter(user=user)
    return render(request, 'view_recommendations.html', {
        'recommendations': recommendations,
        'user': user
    })

def delete_recommendation(request, recommendation_id):
    try:
        recommendation = RecommendedExercise.objects.get(id=recommendation_id)
        recommendation.delete()
        messages.success(request, 'Recommendation deleted successfully.')
    except RecommendedExercise.DoesNotExist:
        messages.error(request, 'Recommendation not found.')

    # Redirect back to the recommendations view
    return redirect('view_recommendations', user=request.user)