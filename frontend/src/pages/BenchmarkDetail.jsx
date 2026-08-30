import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { benchmarkApi } from "../api";
import "../styles.css";

export default function BenchmarkDetail() {
  const { code } = useParams();
  const [benchmark, setBenchmark] = useState(null);
  const [rates, setRates] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    benchmarkApi
      .detail(code)
      .then(({ data }) => setBenchmark(data))
      .catch(() => setError("Benchmark not found"));
    benchmarkApi
      .rates(code)
      .then(({ data }) => setRates(data.results || []))
      .catch(() => setError("Failed to load rates"));
  }, [code]);

  if (error) return <div className="alert alert-error">{error}</div>;
  if (!benchmark) return <p className="loading">Loading...</p>;

  return (
    <div>
      <h1 className="page-title">{benchmark.name}</h1>
      <p className="subtitle">
        {benchmark.code} · {benchmark.currency}
      </p>

      <div className="card">
        <p>{benchmark.description || "No description available."}</p>
        <p>
          <strong>Type:</strong> {benchmark.benchmark_type?.name || "-"} ·{" "}
          <strong>Status:</strong> {benchmark.is_active ? "Active" : "Inactive"}
        </p>
      </div>

      <h2 className="page-title">Rate History</h2>
      <div className="table-wrap">
        <table className="data-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Tenor</th>
              <th>Value</th>
              <th>Source</th>
            </tr>
          </thead>
          <tbody>
            {rates.map((rate, i) => (
              <tr key={`${rate.id}-${i}`}>
                <td>{rate.effective_date}</td>
                <td>{rate.tenor || "-"}</td>
                <td>{rate.value}</td>
                <td>{rate.source || "-"}</td>
              </tr>
            ))}
            {rates.length === 0 && (
              <tr>
                <td colSpan="4" className="empty-row">
                  No rates recorded yet
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}