"""Reports API routes."""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.ReportListCreateView.as_view(), name="report-list"),
    path("schedules/", views.ScheduleListCreateView.as_view(), name="schedule-list"),
    path("<int:pk>/", views.ReportDetailView.as_view(), name="report-detail"),
    path("<int:pk>/generate/", views.ReportGenerationView.as_view(), name="report-generate"),
    path("<int:pk>/export/", views.ReportExportView.as_view(), name="report-export"),
]