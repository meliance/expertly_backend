from django.db import models
from appointment.models import Client, Schedule  # Ensure this import is correct

class Appointment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='appointments')  # Added related_name
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='appointments')  # Added related_name
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ])
    description = models.TextField()

    def __str__(self):
        return f'Appointment for {self.client.name} on {self.schedule.start_time}'

class Notification(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='notifications')  # Added related_name
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=[
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('success', 'Success'),
        ('error', 'Error'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification: {self.title} - {self.message}'