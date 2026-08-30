"""Benchmark API views."""

from django.db import models
from rest_framework import generics, filters, views
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Benchmark, BenchmarkType, BenchmarkRate
from .serializers import (
    BenchmarkSerializer,
    BenchmarkTypeSerializer,
    BenchmarkRateSerializer,
)
from .services import validate_rate


class BenchmarkTypeListView(generics.ListAPIView):
    queryset = BenchmarkType.objects.all()
    serializer_class = BenchmarkTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BenchmarkListCreateView(generics.ListCreateAPIView):
    queryset = Benchmark.objects.select_related("benchmark_type")
    serializer_class = BenchmarkSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["is_active", "currency", "benchmark_type"]
    search_fields = ["name", "code"]
    ordering_fields = ["code", "name", "created_at"]


class BenchmarkDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Benchmark.objects.select_related("benchmark_type")
    serializer_class = BenchmarkSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "code"


class RateListCreateView(generics.ListCreateAPIView):
    serializer_class = BenchmarkRateSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["tenor", "effective_date"]
    ordering_fields = ["effective_date", "value"]
    ordering = ["-effective_date"]

    def get_queryset(self):
        return BenchmarkRate.objects.filter(
            benchmark__code=self.kwargs["code"]
        ).select_related("benchmark")

    def perform_create(self, serializer):
        benchmark = Benchmark.objects.get(code=self.kwargs["code"])
        issues = validate_rate(
            benchmark,
            serializer.validated_data.get("value"),
            serializer.validated_data.get("tenor", ""),
        )
        if any(issue["severity"] == "error" for issue in issues):
            messages = [issue["message"] for issue in issues]
            raise ValidationError({"detail": messages})
        serializer.save(benchmark=benchmark, submitted_by=self.request.user)

    def create(self, request, *args, **kwargs):
        benchmark = Benchmark.objects.get(code=self.kwargs["code"])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        issues = validate_rate(
            benchmark,
            serializer.validated_data.get("value"),
            serializer.validated_data.get("tenor", ""),
        )
        response = super().create(request, *args, **kwargs)
        if issues:
            response.data["validation_warnings"] = [
                issue["message"] for issue in issues if issue["severity"] == "warning"
            ]
        return response


class AnalyticsView(views.APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        """Dashboard aggregations across benchmarks."""
        date_to = request.query_params.get("to")
        date_from = request.query_params.get("from")

        rates = BenchmarkRate.objects.select_related("benchmark", "benchmark__benchmark_type")
        if date_from:
            rates = rates.filter(effective_date__gte=date_from)
        if date_to:
            rates = rates.filter(effective_date__lte=date_to)

        current = rates.order_by("-effective_date").first()

        latest_by_benchmark = (
            BenchmarkRate.objects.filter(
                pk__in=rates.values("benchmark_id")
                .annotate(max=models.Max("id"))
                .values("max")
            )
            .select_related("benchmark")
        )

        top_movers = sorted(
            latest_by_benchmark,
            key=lambda r: abs(r.value),
            reverse=True,
        )[:10]

        return Response({
            "total_benchmarks": Benchmark.objects.filter(is_active=True).count(),
            "total_rates": rates.count(),
            "latest_rate": {
                "benchmark": current.benchmark.code,
                "value": str(current.value),
                "tenor": current.tenor,
                "date": current.effective_date,
            } if current else None,
            "top_movers": [
                {
                    "benchmark": rate.benchmark.code,
                    "value": str(rate.value),
                    "tenor": rate.tenor,
                    "date": rate.effective_date,
                }
                for rate in top_movers
            ],
            "by_currency": list(
                Benchmark.objects.filter(is_active=True)
                .values("currency")
                .annotate(count=models.Count("id"))
            ),
            "by_type": list(
                BenchmarkType.objects.annotate(count=models.Count("benchmarks"))
                .values("code", "name", "count")
            ),
        })