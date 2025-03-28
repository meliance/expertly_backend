from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class User(AbstractUser):
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(_('email address'), unique=True)
    is_client = models.BooleanField(default=False)
    is_expert = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class ClientRegistration(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=63, blank=True)

class ExpertRegistration(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, primary_key=True)
    expertise = models.CharField(max_length=120)
    bio = models.TextField()
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    experience_years = models.IntegerField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
