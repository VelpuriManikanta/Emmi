"""Benchmark API serializers."""

from rest_framework import serializers
from .models import Benchmark, BenchmarkType, BenchmarkRate, ValidationRule


class BenchmarkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BenchmarkType
        fields = ["id", "name", "code", "description"]


class BenchmarkSerializer(serializers.ModelSerializer):
    benchmark_type = BenchmarkTypeSerializer(read_only=True)
    benchmark_type_id = serializers.PrimaryKeyRelatedField(
        queryset=BenchmarkType.objects.all(), source="benchmark_type", write_only=True
    )

    class Meta:
        model = Benchmark
        fields = [
            "id",
            "name",
            "code",
            "benchmark_type",
            "benchmark_type_id",
            "currency",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class BenchmarkRateSerializer(serializers.ModelSerializer):
    benchmark_code = serializers.CharField(source="benchmark.code", read_only=True)

    class Meta:
        model = BenchmarkRate
        fields = [
            "id",
            "benchmark",
            "benchmark_code",
            "value",
            "tenor",
            "effective_date",
            "source",
            "submitted_by",
            "created_at",
        ]
        read_only_fields = ["id", "submitted_by", "created_at"]


class ValidationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidationRule
        fields = [
            "id",
            "benchmark",
            "rule_type",
            "min_value",
            "max_value",
            "max_change_pct",
            "is_active",
        ]
        read_only_fields = ["id"]