"""Reporting data models."""

from django.db import models
from django.contrib.auth.models import User
from benchmarks.models import Benchmark


class Report(models.Model):
    """Generated report document."""

    REPORT_TYPES = [
        ("DAILY", "Daily Report"),
        ("WEEKLY", "Weekly Report"),
        ("MONTHLY", "Monthly Report"),
        ("CUSTOM", "Custom"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("GENERATING", "Generating"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
    ]

    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    generated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    start_date = models.DateField()
    end_date = models.DateField()
    benchmarks = models.ManyToManyField(Benchmark, related_name="reports")
    data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["report_type", "start_date", "end_date"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.created_at:%Y-%m-%d})"


class ReportSchedule(models.Model):
    """Scheduled recurring report generation."""

    FREQUENCIES = [
        ("DAILY", "Daily"),
        ("WEEKLY", "Weekly"),
        ("MONTHLY", "Monthly"),
    ]

    name = models.CharField(max_length=100)
    report_type = models.CharField(max_length=20, choices=Report.REPORT_TYPES)
    frequency = models.CharField(max_length=20, choices=FREQUENCIES)
    benchmarks = models.ManyToManyField(Benchmark, related_name="schedules")
    recipients = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    next_run = models.DateTimeField()
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.frequency}"