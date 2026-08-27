"""Benchmark data models."""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class BenchmarkType(models.Model):
    """Category of benchmark instrument."""

    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Benchmark(models.Model):
    """Individual benchmark instrument or rate."""

    name = models.CharField(max_length=200)
    code = models.SlugField(max_length=50, unique=True)
    benchmark_type = models.ForeignKey(
        BenchmarkType, on_delete=models.PROTECT, related_name="benchmarks"
    )
    currency = models.CharField(max_length=3, default="EUR")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.currency}"


class BenchmarkRate(models.Model):
    """Time series of benchmark rate values."""

    benchmark = models.ForeignKey(
        Benchmark, on_delete=models.CASCADE, related_name="rates"
    )
    value = models.DecimalField(max_digits=18, decimal_places=6)
    tenor = models.CharField(max_length=20, blank=True, help_text="e.g. ON, 1W, 1M, 3M")
    effective_date = models.DateField(db_index=True)
    source = models.CharField(max_length=100, blank=True)
    submitted_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-effective_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["benchmark", "tenor", "effective_date"],
                name="unique_benchmark_rate",
            )
        ]
        indexes = [
            models.Index(fields=["benchmark", "effective_date"]),
        ]

    def __str__(self):
        return f"{self.benchmark.code} {self.tenor} {self.effective_date}: {self.value}"


class ValidationRule(models.Model):
    """Business rules for validating rate submissions."""

    RULE_TYPES = [
        ("RANGE", "Range Check"),
        ("CHANGE", "Variance Check"),
        ("REQUIRED", "Required Field"),
        ("CUSTOM", "Custom"),
    ]

    benchmark = models.ForeignKey(
        Benchmark, on_delete=models.CASCADE, related_name="validation_rules"
    )
    rule_type = models.CharField(max_length=20, choices=RULE_TYPES)
    min_value = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    max_value = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    max_change_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["benchmark", "rule_type"]

    def __str__(self):
        return f"{self.benchmark.code} - {self.rule_type}"