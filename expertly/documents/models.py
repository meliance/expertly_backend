from django.db import models
from accounts.models import Expert
from django.core.validators import FileExtensionValidator, ValidationError
from django.utils import timezone

class ExpertDocument(models.Model):
    DOCUMENT_TYPES = (
        ('license', 'Professional License'),
        ('degree', 'Academic Degree'),
        ('certificate', 'Professional Certificate'),
        ('cv', 'Curriculum Vitae'),
    )
    
    expert = models.ForeignKey(
        Expert,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    document_type = models.CharField(
        max_length=20, 
        choices=DOCUMENT_TYPES
    )
    file = models.FileField(
        upload_to='expert_documents/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text='Only PDF files are allowed (max 5MB)'
    )
    version = models.PositiveSmallIntegerField(
        default=1,
        help_text='Version number for documents of the same type'
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Expert Document'
        verbose_name_plural = 'Expert Documents'
        ordering = ['-uploaded_at']
        unique_together = ('expert', 'document_type', 'version')

    def __str__(self):
        return f"{self.get_document_type_display()} v{self.version} - {self.expert.user.username}"

    def save(self, *args, **kwargs):
        # Auto-increment version if document of same type exists
        if not self.pk:  # Only for new documents
            same_type_docs = ExpertDocument.objects.filter(
                expert=self.expert,
                document_type=self.document_type
            ).count()
            self.version = same_type_docs + 1
        super().save(*args, **kwargs)

    def clean(self):
        # Validate file size (5MB limit)
        if self.file and self.file.size > 5 * 1024 * 1024:
            raise ValidationError("File size must be less than 5MB.")