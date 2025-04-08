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
    CONSULTATION_FIELDS = [
        ('law', 'Legal Consultation'),
        ('tech', 'Technology Consultation'),
        ('financial & business', 'Financial and Business Consultation'),
        ('personal_dev', 'Personal Development Consultation'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='expert_profile'
    )
    
    # Consultation Fields
    consultation_fields = models.JSONField(
        default=list,
        help_text="List of consultation fields this expert specializes in"
    )
    specialization = models.CharField(max_length=100, blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    experience_years = models.IntegerField(blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    experience_years = models.IntegerField(default=0)
    
    # Status fields
    is_approved = models.BooleanField(
        default=False,
        help_text="Whether the expert has been approved by admin"
    )
    approval_date = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="Date when expert was approved"
    )
    
    # Rating system
    rating = models.FloatField(
        default=0.0, 
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        help_text="Average rating from 0-5"
    )
    total_sessions = models.PositiveIntegerField(
        default=0,
        help_text="Total consultation sessions completed"
    )
    
    class Meta:
        verbose_name = 'Expert'
        verbose_name_plural = 'Experts'
        ordering = ['-is_approved', '-rating']
        indexes = [
            models.Index(fields=['consultation_fields'], name='consult_fields_idx'),
        ]

    def __str__(self):
        return f"Expert: {self.user.get_full_name() or self.user.username} ({self.specialization})"
    
    def get_consultation_fields_display(self):
        """Returns human-readable consultation fields"""
        return ", ".join([dict(self.CONSULTATION_FIELDS).get(field, field) 
                         for field in self.consultation_fields])
    
    def save(self, *args, **kwargs):
        # Validate consultation_fields contains only valid choices
        if self.consultation_fields:
            valid_fields = [choice[0] for choice in self.CONSULTATION_FIELDS]
            if not all(field in valid_fields for field in self.consultation_fields):
                raise ValueError("Invalid consultation field provided")
        
        super().save(*args, **kwargs)
    
    @property
    def display_rate(self):
        """Formatted hourly rate"""
        return f"${self.hourly_rate:.2f}/hr"
    
    @property
    def experience_level(self):
        """Categorize experience level"""
        if not self.experience_years:
            return "Not specified"
        if self.experience_years < 3:
            return "Junior"
        if self.experience_years < 7:
            return "Mid-level"
        return "Senior"