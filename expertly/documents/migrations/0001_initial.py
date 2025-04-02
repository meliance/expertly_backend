# Generated by Django 5.1.7 on 2025-04-01 07:38

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0003_delete_expertdocument"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExpertDocument",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "document_type",
                    models.CharField(
                        choices=[
                            ("license", "Professional License"),
                            ("degree", "Academic Degree"),
                            ("certificate", "Professional Certificate"),
                            ("cv", "Curriculum Vitae"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        help_text="Only PDF files are allowed (max 5MB)",
                        upload_to="expert_documents/%Y/%m/%d/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["pdf"]
                            )
                        ],
                    ),
                ),
                (
                    "version",
                    models.PositiveSmallIntegerField(
                        default=1,
                        help_text="Version number for documents of the same type",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                ("is_verified", models.BooleanField(default=False)),
                (
                    "uploaded_at",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "expert",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="documents",
                        to="accounts.expert",
                    ),
                ),
            ],
            options={
                "verbose_name": "Expert Document",
                "verbose_name_plural": "Expert Documents",
                "ordering": ["-uploaded_at"],
                "unique_together": {("expert", "document_type", "version")},
            },
        ),
    ]
