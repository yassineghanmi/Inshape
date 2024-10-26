
from django.db import models

class Routine(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    details = models.TextField()  # To hold the generated workout routine details
    image = models.ImageField(upload_to='routine_images/', null=True, blank=True)  # Add this line

    def __str__(self):
        return self.name
