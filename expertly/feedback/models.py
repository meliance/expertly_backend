from django.db import models
from appointment.models import Client, Schedule, Appointment  # Import necessary models

class Expert(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Feedback(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # Assuming rating is from 1 to 5
    review = models.TextField()

    def __str__(self):
        return f'Feedback from {self.client.name} for {self.expert.name}'