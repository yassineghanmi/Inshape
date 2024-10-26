# workouts/forms.py

from django import forms

MUSCLE_GROUP_CHOICES = [
    ('Chest', 'Chest'),
    ('Back', 'Back'),
    ('Legs', 'Legs'),
    ('Shoulders', 'Shoulders'),
    ('Arms', 'Arms'),
    ('Abdominals', 'Abdominals'),
]

LEVEL_CHOICES = [
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced'),
]


class RecommendationForm(forms.Form):
    user = forms.CharField(max_length=100, label="User Name")
    muscle_group = forms.ChoiceField(choices=MUSCLE_GROUP_CHOICES, label="Muscle Group")
    level = forms.ChoiceField(choices=LEVEL_CHOICES, label="Experience Level")
    total_exercises = forms.IntegerField(min_value=1, max_value=10, label="Number of Exercises")
