import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import os
from django.core.validators import MinValueValidator, FileExtensionValidator

def user_directory_path(instance, filename):
    """File upload path for user-related documents"""
    return f'users/{instance.user.id}/documents/{filename}'

def profile_picture_path(instance, filename):
    """File upload path for profile pictures"""
    return f'users/{instance.id}/profile/{filename}'

class User(AbstractUser):
    # Authentication fields
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    is_client = models.BooleanField(default=False)
    is_expert = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Profile fields
    profile_picture = models.ImageField(
        upload_to=profile_picture_path,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    address = models.TextField(blank=True)
    
    # Login fields
    last_login = models.DateTimeField(null=True, blank=True)
    last_logout = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.email})"

    def save(self, *args, **kwargs):
        # Ensure email is lowercase
        self.email = self.email.lower()
        super().save(*args, **kwargs)

class ClientRegistration(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='client_profile'
    )
    bio = models.TextField(blank=True, help_text="Tell us about yourself")
    location = models.CharField(
        max_length=100,
        blank=True,
        help_text="Your primary location"
    )
    preferred_communication = models.CharField(
        max_length=20,
        choices=[('email', 'Email'), ('phone', 'Phone'), ('both', 'Both')],
        default='email'
    )

    class Meta:
        verbose_name = "Client Profile"
        verbose_name_plural = "Client Profiles"
        ordering = ['user__created_at']

    def __str__(self):
        return f"{self.user.get_full_name()}'s Client Profile"

class ExpertRegistration(models.Model):
    DOCUMENT_TYPES = [
        ('license', 'Professional License'),
        ('degree', 'Academic Degree'),
        ('certificate', 'Professional Certificate'),
        ('id_proof', 'Government ID'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='expert_profile'
    )
    expertise = models.CharField(
        max_length=120,
        help_text="Your primary area of expertise"
    )
    bio = models.TextField(help_text="Detailed professional bio")
    hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Your hourly rate in USD"
    )
    experience_years = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Years of professional experience"
    )
    
    # Verification status
    is_approved = models.BooleanField(default=False)
    approval_date = models.DateTimeField(null=True, blank=True)
    
    # Document fields with validation
    license_file = models.FileField(
        upload_to=user_directory_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])]
    )
    degree_file = models.FileField(
        upload_to=user_directory_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])]
    )
    certificate_file = models.FileField(
        upload_to=user_directory_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])]
    )
    id_proof_file = models.FileField(
        upload_to=user_directory_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])]
    )
    
    # Verification tracking
    documents_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    verification_notes = models.TextField(blank=True)
    
    # Availability
    is_available = models.BooleanField(default=True)
    available_from = models.TimeField(null=True, blank=True)
    available_to = models.TimeField(null=True, blank=True)
    
    # Additional professional details
    specialties = models.TextField(
        blank=True,
        help_text="List your specialties separated by commas"
    )
    languages = models.CharField(
        max_length=255,
        blank=True,
        default="English",
        help_text="Languages you speak (comma separated)"
    )

    class Meta:
        verbose_name = "Expert Profile"
        verbose_name_plural = "Expert Profiles"
        ordering = ['-is_approved', 'user__created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.expertise} (${self.hourly_rate}/hr)"