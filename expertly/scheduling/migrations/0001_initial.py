# Generated by Django 5.1.7 on 2025-04-07 14:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TimeOff",
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
                ("start_datetime", models.DateTimeField()),
                ("end_datetime", models.DateTimeField()),
                ("reason", models.TextField(blank=True, null=True)),
                (
                    "expert",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="time_offs",
                        to="accounts.expert",
                    ),
                ),
            ],
            options={
                "ordering": ["start_datetime"],
            },
        ),
        migrations.CreateModel(
            name="Schedule",
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
                    "day_of_week",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "Monday"),
                            (1, "Tuesday"),
                            (2, "Wednesday"),
                            (3, "Thursday"),
                            (4, "Friday"),
                            (5, "Saturday"),
                            (6, "Sunday"),
                        ]
                    ),
                ),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                ("duration", models.PositiveSmallIntegerField()),
                ("is_available", models.BooleanField(default=True)),
                (
                    "expert",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="schedules",
                        to="accounts.expert",
                    ),
                ),
            ],
            options={
                "ordering": ["day_of_week", "start_time"],
                "unique_together": {
                    ("expert", "day_of_week", "start_time", "end_time")
                },
            },
        ),
    ]
