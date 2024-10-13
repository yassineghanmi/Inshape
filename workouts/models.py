from django.db import models

class Exercise(models.Model):
    title = models.CharField(max_length=100)
    body_part = models.CharField(max_length=50)
    equipment = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class RecommendedExercise(models.Model):
    exercises = models.ManyToManyField(Exercise)  # Multiple exercises per recommendation
    muscle_group = models.CharField(max_length=100, default='General')  # New field for muscle group
    user = models.CharField(max_length=100)  # Store user info here (could link to User model)

    def __str__(self):
        return f"Recommendation for {self.user} (Muscle Group: {self.muscle_group})"
