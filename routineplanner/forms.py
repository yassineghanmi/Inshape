from django import forms

class RoutineForm(forms.Form):
    goal = forms.ChoiceField(choices=[('muscle gain', 'Muscle Gain'), ('weight loss', 'Weight Loss')])
    experience_level = forms.ChoiceField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')])
    duration = forms.IntegerField(min_value=1, max_value=12)  # Duration in weeks
    workout_type = forms.ChoiceField(choices=[('strength', 'Strength'), ('endurance', 'Endurance')])
    target_muscle_groups = forms.MultipleChoiceField(choices=[('chest', 'Chest'), ('back', 'Back'), ('legs', 'Legs'), ('arms', 'Arms')])
    equipment_needed = forms.MultipleChoiceField(choices=[('dumbbells', 'Dumbbells'), ('barbell', 'Barbell'), ('bench', 'Bench'), ('kettlebell', 'Kettlebell')])
    sessions_per_week = forms.IntegerField(min_value=1, max_value=7)
   