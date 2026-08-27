"""Reports API serializers."""

from rest_framework import serializers
from benchmarks.models import Benchmark
from .models import Report, ReportSchedule


class ReportSerializer(serializers.ModelSerializer):
    benchmarks = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="code"
    )
    benchmark_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        source="benchmarks",
        queryset=Benchmark.objects.all(),
        required=False,
    )

    class Meta:
        model = Report
        fields = [
            "id",
            "title",
            "report_type",
            "status",
            "generated_by",
            "start_date",
            "end_date",
            "benchmarks",
            "benchmark_ids",
            "data",
            "created_at",
            "completed_at",
        ]
        read_only_fields = ["id", "status", "generated_by", "created_at", "completed_at"]


class ReportScheduleSerializer(serializers.ModelSerializer):
    benchmarks = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="code"
    )
    benchmark_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        source="benchmarks",
        queryset=Benchmark.objects.all(),
        required=False,
    )

    class Meta:
        model = ReportSchedule
        fields = [
            "id",
            "name",
            "report_type",
            "frequency",
            "benchmarks",
            "benchmark_ids",
            "recipients",
            "is_active",
            "next_run",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at"]