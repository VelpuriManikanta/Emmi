"""Benchmark API routes."""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.BenchmarkListCreateView.as_view(), name="benchmark-list"),
    path("<slug:code>/", views.BenchmarkDetailView.as_view(), name="benchmark-detail"),
    path("<slug:code>/rates/", views.RateListCreateView.as_view(), name="rate-list"),
    path("types/", views.BenchmarkTypeListView.as_view(), name="benchmark-type-list"),
]