from django.db import models
from accounts.models import Expert

class Schedule(models.Model):
    DAY_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.PositiveSmallIntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration = models.PositiveSmallIntegerField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('expert', 'day_of_week', 'start_time', 'end_time')
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.expert.user.username} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"

class TimeOff(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name='time_offs')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    reason = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['start_datetime']

    def __str__(self):
        return f"{self.expert.user.username} - Time off from {self.start_datetime} to {self.end_datetime}"