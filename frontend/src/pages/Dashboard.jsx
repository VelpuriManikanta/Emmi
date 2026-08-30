import { useEffect, useState } from "react";
import { benchmarkApi } from "../api";
import "../styles.css";

export default function Dashboard() {
  const [analytics, setAnalytics] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    benchmarkApi
      .analytics()
      .then(({ data }) => setAnalytics(data))
      .catch(() => setError("Failed to load dashboard data"));
  }, []);

  if (error) return <div className="alert alert-error">{error}</div>;
  if (!analytics) return <p className="loading">Loading dashboard...</p>;

  const cards = [
    { label: "Active Benchmarks", value: analytics.total_benchmarks },
    { label: "Total Rates", value: analytics.total_rates },
  ];

  return (
    <div>
      <h1 className="page-title">Dashboard</h1>

      <div className="card-grid">
        {cards.map((card) => (
          <div className="stat-card" key={card.label}>
            <span className="stat-label">{card.label}</span>
            <span className="stat-value">{card.value}</span>
          </div>
        ))}
      </div>

      {analytics.latest_rate && (
        <div className="card">
          <h3>Latest Rate</h3>
          <p>
            <strong>{analytics.latest_rate.benchmark}</strong> {analytics.latest_rate.tenor} —{" "}
            {analytics.latest_rate.value} on {analytics.latest_rate.date}
          </p>
        </div>
      )}

      <div className="card-grid">
        <div className="card">
          <h3>Rates by Currency</h3>
          <ul className="simple-list">
            {analytics.by_currency.map((c) => (
              <li key={c.currency}>
                {c.currency}: {c.count}
              </li>
            ))}
          </ul>
        </div>

        <div className="card">
          <h3>Top Movers</h3>
          <ul className="simple-list">
            {analytics.top_movers.map((m) => (
              <li key={`${m.benchmark}-${m.date}`}>
                {m.benchmark} ({m.tenor}): {m.value}
              </li>
            ))}
          </ul>
        </div>
      </div>

      <h2 className="page-title">Benchmarks by Type</h2>
      <div className="card">
        <ul className="simple-list">
          {analytics.by_type.map((t) => (
            <li key={t.code}>
              {t.name}: {t.count} benchmarks
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}