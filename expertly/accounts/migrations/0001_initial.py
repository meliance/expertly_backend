# Generated by Django 5.1.7 on 2025-04-07 14:59

import accounts.models
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "user_type",
                    models.CharField(
                        choices=[("client", "Client"), ("expert", "Expert")],
                        default="client",
                        max_length=10,
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=20, null=True, unique=True),
                ),
                (
                    "profile_picture",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=accounts.models.profile_picture_path,
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                ["jpg", "jpeg", "png"]
                            )
                        ],
                    ),
                ),
                ("is_verified", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("last_login", models.DateTimeField(blank=True, null=True)),
                ("last_logout", models.DateTimeField(blank=True, null=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "Users",
                "ordering": ["-created_at"],
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="client_profile",
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Client",
                "verbose_name_plural": "Clients",
                "ordering": ["user__created_at"],
            },
        ),
        migrations.CreateModel(
            name="Expert",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="expert_profile",
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "consultation_fields",
                    models.JSONField(
                        default=list,
                        help_text="List of consultation fields this expert specializes in",
                    ),
                ),
                (
                    "specialization",
                    models.CharField(
                        help_text="Primary professional specialization", max_length=100
                    ),
                ),
                (
                    "qualifications",
                    models.TextField(
                        help_text="Certifications, degrees, and other qualifications"
                    ),
                ),
                (
                    "experience_years",
                    models.PositiveIntegerField(
                        blank=True,
                        help_text="Years of professional experience",
                        null=True,
                    ),
                ),
                (
                    "hourly_rate",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Hourly consultation rate in local currency",
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "is_approved",
                    models.BooleanField(
                        default=False,
                        help_text="Whether the expert has been approved by admin",
                    ),
                ),
                (
                    "approval_date",
                    models.DateTimeField(
                        blank=True, help_text="Date when expert was approved", null=True
                    ),
                ),
                (
                    "rating",
                    models.FloatField(
                        default=0.0,
                        help_text="Average rating from 0-5",
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(5.0),
                        ],
                    ),
                ),
                (
                    "total_sessions",
                    models.PositiveIntegerField(
                        default=0, help_text="Total consultation sessions completed"
                    ),
                ),
            ],
            options={
                "verbose_name": "Expert",
                "verbose_name_plural": "Experts",
                "ordering": ["-is_approved", "-rating"],
                "indexes": [
                    models.Index(
                        fields=["consultation_fields"], name="consult_fields_idx"
                    )
                ],
            },
        ),
    ]
