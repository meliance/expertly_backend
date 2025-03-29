from django.db import models

class Expert(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField()
    daily_availability = models.BooleanField(default=False)

    def __str__(self):
        return f'Schedule for {self.expert.name} from {self.start_time} to {self.end_time}'

class Client(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('canceled', 'Canceled')])
    description = models.TextField()

    def __str__(self):
        return f'Appointment for {self.client.name} on {self.schedule.start_time}'