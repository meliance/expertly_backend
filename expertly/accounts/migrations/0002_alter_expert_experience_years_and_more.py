# Generated by Django 5.1.7 on 2025-04-08 10:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expert",
            name="experience_years",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="expert",
            name="hourly_rate",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=6, null=True
            ),
        ),
        migrations.AlterField(
            model_name="expert",
            name="qualifications",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="expert",
            name="specialization",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
