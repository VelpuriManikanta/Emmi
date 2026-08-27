"""Django admin for benchmarks."""

from django.contrib import admin
from .models import Benchmark, BenchmarkType, BenchmarkRate, ValidationRule


@admin.register(BenchmarkType)
class BenchmarkTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]
    search_fields = ["name", "code"]


@admin.register(Benchmark)
class BenchmarkAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "benchmark_type", "currency", "is_active"]
    list_filter = ["benchmark_type", "currency", "is_active"]
    search_fields = ["code", "name"]
    prepopulated_fields = {"code": ("name",)}


@admin.register(BenchmarkRate)
class BenchmarkRateAdmin(admin.ModelAdmin):
    list_display = ["benchmark", "tenor", "value", "effective_date", "source"]
    list_filter = ["tenor", "effective_date", "benchmark"]
    search_fields = ["benchmark__code", "source"]
    date_hierarchy = "effective_date"


@admin.register(ValidationRule)
class ValidationRuleAdmin(admin.ModelAdmin):
    list_display = ["benchmark", "rule_type", "min_value", "max_value", "is_active"]
    list_filter = ["rule_type", "is_active"]