import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { benchmarkApi } from "../api";
import "../styles.css";

const COLORS = ["#1f4e8c", "#2e86de", "#5dade2", "#85c1e9", "#aed6f1", "#1e9e6a", "#27ae60", "#82e0aa"];

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

  const currencyData = analytics.by_currency.map((c) => ({
    name: c.currency,
    count: c.count,
  }));

  const typeData = analytics.by_type.map((t) => ({
    name: t.code,
    fullName: t.name,
    count: t.count,
  }));

  const moversData = analytics.top_movers.map((m) => ({
    name: m.benchmark,
    value: parseFloat(m.value),
    tenor: m.tenor,
  }));

  return (
    <div>
      <h1 className="page-title">Dashboard</h1>

      <div className="card-grid">
        <div className="stat-card">
          <span className="stat-label">Active Benchmarks</span>
          <span className="stat-value">{analytics.total_benchmarks}</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Total Rates Recorded</span>
          <span className="stat-value">{analytics.total_rates}</span>
        </div>
        {analytics.latest_rate && (
          <div className="stat-card stat-card-highlight">
            <span className="stat-label">Latest Rate</span>
            <span className="stat-value">
              {analytics.latest_rate.value}
            </span>
            <span className="stat-sub">
              {analytics.latest_rate.benchmark} {analytics.latest_rate.tenor} · {analytics.latest_rate.date}
            </span>
          </div>
        )}
      </div>

      <div className="chart-grid">
        {moversData.length > 0 && (
          <div className="card">
            <h3>Top Movers</h3>
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={moversData} margin={{ top: 10, right: 20, left: 10, bottom: 0 }}>
                <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                  {moversData.map((_, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {currencyData.length > 0 && (
          <div className="card">
            <h3>Rates by Currency</h3>
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={currencyData} margin={{ top: 10, right: 20, left: 10, bottom: 0 }}>
                <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="count" radius={[4, 4, 0, 0]} fill="#1e9e6a" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {typeData.length > 0 && (
          <div className="card">
            <h3>Benchmarks by Type</h3>
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={typeData} margin={{ top: 10, right: 20, left: 10, bottom: 0 }}>
                <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip formatter={(value, name, props) => [value, props.payload.fullName]} />
                <Bar dataKey="count" radius={[4, 4, 0, 0]} fill="#2e86de" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {analytics.latest_rate && (
        <div className="card">
          <h3>Latest Submissions</h3>
          <table className="data-table">
            <thead>
              <tr>
                <th>Benchmark</th>
                <th>Tenor</th>
                <th>Value</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {analytics.top_movers.map((m) => (
                <tr key={`${m.benchmark}-${m.tenor}-${m.date}`}>
                  <td>{m.benchmark}</td>
                  <td>{m.tenor}</td>
                  <td className="mono">{m.value}</td>
                  <td>{m.date}</td>
                </tr>
              ))}
              {analytics.top_movers.length === 0 && (
                <tr>
                  <td colSpan="4" className="empty-row">No rates recorded yet</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}