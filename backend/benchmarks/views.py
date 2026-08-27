"""Benchmark API views."""

from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Benchmark, BenchmarkType, BenchmarkRate
from .serializers import (
    BenchmarkSerializer,
    BenchmarkTypeSerializer,
    BenchmarkRateSerializer,
)


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
    filterset_fields = ["tenor", "effective_date", "effective_date__gte", "effective_date__lte"]
    ordering_fields = ["effective_date", "value"]
    ordering = ["-effective_date"]

    def get_queryset(self):
        return BenchmarkRate.objects.filter(
            benchmark__code=self.kwargs["code"]
        ).select_related("benchmark")

    def perform_create(self, serializer):
        benchmark = Benchmark.objects.get(code=self.kwargs["code"])
        serializer.save(benchmark=benchmark, submitted_by=self.request.user)