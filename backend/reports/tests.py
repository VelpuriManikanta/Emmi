"""Tests for report models."""

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Report, ReportSchedule


class ReportModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="reportuser", password="testpass123"
        )

    def test_create_report(self):
        report = Report.objects.create(
            title="Daily EURIBOR Report",
            report_type="DAILY",
            status="COMPLETED",
            generated_by=self.user,
            start_date="2024-01-01",
            end_date="2024-01-31",
        )
        self.assertEqual(
            str(report), f"Daily EURIBOR Report ({report.created_at:%Y-%m-%d})"
        )
        self.assertEqual(report.data, {})

    def test_create_schedule(self):
        schedule = ReportSchedule.objects.create(
            name="Weekly Summary",
            report_type="WEEKLY",
            frequency="WEEKLY",
            next_run="2024-02-01T09:00:00Z",
            created_by=self.user,
        )
        self.assertEqual(str(schedule), "Weekly Summary - WEEKLY")
        self.assertTrue(schedule.is_active)