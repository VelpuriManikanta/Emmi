"""Report generation service."""

from django.utils import timezone
from benchmarks.models import Benchmark, BenchmarkRate
from .models import Report


def generate_report(report):
    """Populate report.data with benchmark rates within its date range.

    Uses the report's linked benchmarks, or all active benchmarks when
    none are explicitly configured.
    """
    benchmarks = report.benchmarks.all()
    if not benchmarks:
        benchmarks = Benchmark.objects.filter(is_active=True)

    rates = (
        BenchmarkRate.objects.filter(
            benchmark__in=benchmarks,
            effective_date__gte=report.start_date,
            effective_date__lte=report.end_date,
        )
        .select_related("benchmark")
        .order_by("benchmark__code", "effective_date")
    )

    rows = []
    latest_by_benchmark = {}

    for rate in rates:
        rows.append({
            "benchmark": rate.benchmark.code,
            "value": str(rate.value),
            "tenor": rate.tenor,
            "date": str(rate.effective_date),
            "source": rate.source,
        })
        latest_by_benchmark.setdefault(rate.benchmark.code, []).append(
            [str(rate.effective_date), str(rate.value)]
        )

    report.data = {
        "rows": rows,
        "total_rows": len(rows),
        "series": {
            code: {"dates": [p[0] for p in points], "values": points[0]}
            for code, points in latest_by_benchmark.items()
        },
    }
    report.status = "COMPLETED"
    report.completed_at = timezone.now()
    report.save(update_fields=["data", "status", "completed_at"])
    return report