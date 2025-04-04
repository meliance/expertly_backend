from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MinValueValidator, 
    MaxValueValidator,
    FileExtensionValidator
)

# File upload path functions
def profile_picture_path(instance, filename):
    """Returns path for user profile pictures"""
    return f'users/{instance.id}/profile/{filename}'

def expert_document_path(instance, filename):
    """Returns path for expert documents"""
    return f'experts/{instance.expert.user.id}/documents/{filename}'

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('expert', 'Expert'),
    )

    # Core fields
    user_type = models.CharField(
        max_length=10, 
        choices=USER_TYPE_CHOICES, 
        default='client'
    )
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        unique=True
    )
    
    # Profile fields
    profile_picture = models.ImageField(
        upload_to=profile_picture_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    is_verified = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Authentication fields
    last_login = models.DateTimeField(null=True, blank=True)
    last_logout = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.email})"

    def save(self, *args, **kwargs):
        # Ensure email is lowercase
        self.email = self.email.lower()
        super().save(*args, **kwargs)

class Client(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='client_profile'
    )   
    
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['user__created_at']

    def __str__(self):
        return f"Client: {self.user.username}"

class Expert(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='expert_profile'
    )
    specialization = models.CharField(max_length=100)
    qualifications = models.TextField()
    experience_years = models.PositiveIntegerField(blank=True, null=True)
    hourly_rate = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    # Status fields
    is_approved = models.BooleanField(default=False)
    approval_date = models.DateTimeField(null=True, blank=True)
    
    # Rating system
    rating = models.FloatField(
        default=0.0, 
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    total_sessions = models.PositiveIntegerField(default=0)
    
    # Availability
    is_available = models.BooleanField(default=True)
    available_from = models.TimeField(null=True, blank=True)
    available_to = models.TimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Expert'
        verbose_name_plural = 'Experts'
        ordering = ['-is_approved', '-rating']

    def __str__(self):
        return f"Expert: {self.user.username} ({self.specialization})"