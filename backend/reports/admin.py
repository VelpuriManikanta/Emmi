"""Django admin for reports."""

from django.contrib import admin
from .models import Report, ReportSchedule


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["title", "report_type", "status", "start_date", "end_date", "created_at"]
    list_filter = ["report_type", "status", "created_at"]
    search_fields = ["title"]


@admin.register(ReportSchedule)
class ReportScheduleAdmin(admin.ModelAdmin):
    list_display = ["name", "report_type", "frequency", "is_active", "next_run"]
    list_filter = ["frequency", "is_active"]
    search_fields = ["name"]