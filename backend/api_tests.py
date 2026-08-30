"""API endpoint tests."""

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from benchmarks.models import Benchmark, BenchmarkType, BenchmarkRate, ValidationRule
from reports.models import Report


class BaseAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="apiuser", email="api@test.com", password="testpass123"
        )
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.benchmark_type = BenchmarkType.objects.create(
            name="Interbank Rate", code="IR"
        )
        self.benchmark = Benchmark.objects.create(
            name="EURIBOR 3M",
            code="euribor-3m",
            benchmark_type=self.benchmark_type,
            currency="EUR",
        )


class AuthTests(BaseAPITest):
    def test_register_user(self):
        self.client.force_authenticate(user=None)
        response = self.client.post("/api/auth/register/", {
            "username": "newuser",
            "email": "new@test.com",
            "password": "strongpass123",
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "newuser")

    def test_token_obtain(self):
        self.client.force_authenticate(user=None)
        response = self.client.post("/api/auth/token/", {
            "username": "apiuser",
            "password": "testpass123",
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_me_requires_auth(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BenchmarkAPITests(BaseAPITest):
    def test_list_benchmarks(self):
        response = self.client.get("/api/benchmarks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["code"], "euribor-3m")

    def test_create_benchmark(self):
        response = self.client.post("/api/benchmarks/", {
            "name": "EONIA",
            "code": "eonia",
            "benchmark_type_id": self.benchmark_type.id,
            "currency": "EUR",
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["code"], "eonia")

    def test_get_benchmark_detail(self):
        response = self.client.get("/api/benchmarks/euribor-3m/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "EURIBOR 3M")


class RateAPITests(BaseAPITest):
    def setUp(self):
        super().setUp()
        ValidationRule.objects.create(
            benchmark=self.benchmark,
            rule_type="RANGE",
            min_value="1.0",
            max_value="5.0",
        )

    def test_create_valid_rate(self):
        response = self.client.post(
            f"/api/benchmarks/{self.benchmark.code}/rates/",
            {"value": "3.75", "tenor": "3M", "effective_date": "2024-01-01"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["value"], "3.750000")

    def test_rate_out_of_range_rejected(self):
        response = self.client.post(
            f"/api/benchmarks/{self.benchmark.code}/rates/",
            {"value": "99.99", "tenor": "3M", "effective_date": "2024-01-01"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)

    def test_list_rates(self):
        BenchmarkRate.objects.create(
            benchmark=self.benchmark,
            value="3.75",
            tenor="3M",
            effective_date="2024-01-01",
        )
        response = self.client.get(f"/api/benchmarks/{self.benchmark.code}/rates/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)


class AnalyticsTests(BaseAPITest):
    def test_analytics(self):
        BenchmarkRate.objects.create(
            benchmark=self.benchmark,
            value="3.75",
            tenor="3M",
            effective_date="2024-01-01",
        )
        response = self.client.get("/api/benchmarks/analytics/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_benchmarks"], 1)
        self.assertEqual(response.data["total_rates"], 1)
        self.assertEqual(response.data["latest_rate"]["benchmark"], "euribor-3m")


class ReportAPITests(BaseAPITest):
    def test_create_and_generate_report(self):
        BenchmarkRate.objects.create(
            benchmark=self.benchmark,
            value="3.75",
            tenor="3M",
            effective_date="2024-01-01",
        )
        response = self.client.post("/api/reports/", {
            "title": "Daily Report",
            "report_type": "DAILY",
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "COMPLETED")
        self.assertEqual(response.data["data"]["total_rows"], 1)

    def test_export_report(self):
        rate = BenchmarkRate.objects.create(
            benchmark=self.benchmark,
            value="3.75",
            tenor="3M",
            effective_date="2024-01-01",
        )
        report = Report.objects.create(
            title="Daily Report",
            report_type="DAILY",
            status="COMPLETED",
            generated_by=self.user,
            start_date="2024-01-01",
            end_date="2024-01-31",
            data={"rows": [{
                "benchmark": "euribor-3m",
                "value": "3.75",
                "tenor": "3M",
                "date": "2024-01-01",
                "source": rate.source,
            }]},
        )
        report.benchmarks.add(self.benchmark)
        response = self.client.get(f"/api/reports/{report.id}/export/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("euribor-3m", response.content.decode())