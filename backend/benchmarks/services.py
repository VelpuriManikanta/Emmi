"""Rate validation engine using business rules."""

from decimal import Decimal

from .models import BenchmarkRate, ValidationRule

ERROR_RANGE = "OUT_OF_RANGE"
ERROR_CHANGE = "CHANGE_EXCEEDED"
WARNING = "warning"
ERROR = "error"


def validate_rate(benchmark, value, tenor=""):
    """Validate a rate value against active rules for a benchmark.

    Returns a list of issue dicts: {"severity", "rule", "message"}.
    """
    issues = []
    rules = ValidationRule.objects.filter(benchmark=benchmark, is_active=True)

    for rule in rules:
        if rule.rule_type == "REQUIRED" and (value is None or value == ""):
            issues.append({
                "severity": ERROR,
                "rule": "REQUIRED",
                "message": f"Value is required for {benchmark.code}",
            })

        if value is None or value == "":
            continue

        value = Decimal(value)

        if rule.rule_type == "RANGE":
            if rule.min_value is not None and value < rule.min_value:
                issues.append({
                    "severity": ERROR,
                    "rule": "RANGE",
                    "message": f"Value {value} below minimum {rule.min_value}",
                })
            if rule.max_value is not None and value > rule.max_value:
                issues.append({
                    "severity": ERROR,
                    "rule": "RANGE",
                    "message": f"Value {value} above maximum {rule.max_value}",
                })

        if rule.rule_type == "CHANGE" and rule.max_change_pct is not None:
            latest = (
                BenchmarkRate.objects.filter(benchmark=benchmark, tenor=tenor)
                .order_by("-effective_date")
                .first()
            )
            if latest and latest.value != 0:
                change_pct = (
                    abs(value - latest.value) / abs(latest.value)
                ) * 100
                if change_pct > rule.max_change_pct:
                    issues.append({
                        "severity": ERROR,
                        "rule": "CHANGE",
                        "message": (
                            f"Change {change_pct:.2f}% exceeds "
                            f"limit {rule.max_change_pct}%"
                        ),
                    })

    return issues


def validate_serializer_rate(serializer):
    """Run validation inside serializer.create and return issues."""
    benchmark = serializer.validated_data["benchmark"]
    value = serializer.validated_data.get("value")
    tenor = serializer.validated_data.get("tenor", "")
    return validate_rate(benchmark, value, tenor)