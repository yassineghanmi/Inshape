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
    ('Expert', 'Expert'),
]

class RecommendationForm(forms.Form):
    #user = forms.CharField(max_length=100, label="User Name", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}))
    muscle_group = forms.ChoiceField(choices=MUSCLE_GROUP_CHOICES, label="Muscle Group", widget=forms.Select(attrs={'class': 'form-control'}))
    level = forms.ChoiceField(choices=LEVEL_CHOICES, label="Experience Level", widget=forms.Select(attrs={'class': 'form-control'}))
    total_exercises = forms.IntegerField(min_value=1, max_value=10, label="Number of Exercises", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1 - 10'}))
