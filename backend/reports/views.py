"""Reports API views."""

import csv

from django.http import HttpResponse
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from .models import Report, ReportSchedule
from .serializers import ReportSerializer, ReportScheduleSerializer


class ReportListCreateView(generics.ListCreateAPIView):
    queryset = Report.objects.prefetch_related("benchmarks")
    serializer_class = ReportSerializer

    def perform_create(self, serializer):
        serializer.save(generated_by=self.request.user)


class ReportDetailView(generics.RetrieveDestroyAPIView):
    queryset = Report.objects.prefetch_related("benchmarks")
    serializer_class = ReportSerializer


class ReportExportView(generics.GenericAPIView):
    queryset = Report.objects.prefetch_related("benchmarks")

    def get(self, request, pk):
        report = self.get_object()
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{report.title}.csv"'

        writer = csv.writer(response)
        writer.writerow(["Benchmark", "Tenor", "Value", "Date", "Source"])

        rows = report.data.get("rows", [])
        for row in rows:
            writer.writerow([
                row.get("benchmark", ""),
                row.get("tenor", ""),
                row.get("value", ""),
                row.get("date", ""),
                row.get("source", ""),
            ])

        return response


class ScheduleListCreateView(generics.ListCreateAPIView):
    queryset = ReportSchedule.objects.prefetch_related("benchmarks")
    serializer_class = ReportScheduleSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)