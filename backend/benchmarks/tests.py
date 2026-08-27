"""Tests for benchmark models."""

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Benchmark, BenchmarkType, BenchmarkRate


class BenchmarkModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.benchmark_type = BenchmarkType.objects.create(
            name="Interbank Rate", code="IR"
        )
        self.benchmark = Benchmark.objects.create(
            name="EURIBOR 3M",
            code="euribor-3m",
            benchmark_type=self.benchmark_type,
            currency="EUR",
        )

    def test_benchmark_str(self):
        self.assertEqual(str(self.benchmark), "euribor-3m - EUR")

    def test_benchmark_type_str(self):
        self.assertEqual(str(self.benchmark_type), "Interbank Rate")

    def test_create_rate(self):
        rate = BenchmarkRate.objects.create(
            benchmark=self.benchmark,
            value="3.750000",
            tenor="3M",
            effective_date="2024-01-01",
            source="EMMI",
            submitted_by=self.user,
        )
        self.assertEqual(rate.benchmark, self.benchmark)
        self.assertEqual(str(rate.value), "3.750000")

    def test_duplicate_rate_rejected(self):
        BenchmarkRate.objects.create(
            benchmark=self.benchmark,
            value="3.750000",
            tenor="3M",
            effective_date="2024-01-01",
        )
        with self.assertRaises(Exception):
            BenchmarkRate.objects.create(
                benchmark=self.benchmark,
                value="3.760000",
                tenor="3M",
                effective_date="2024-01-01",
            )