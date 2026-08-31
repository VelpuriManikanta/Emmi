import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { benchmarkApi } from "../api";
import { useToast } from "../context/ToastContext";
import "../styles.css";

export default function BenchmarkDetail() {
  const { code } = useParams();
  const { addToast } = useToast();
  const [benchmark, setBenchmark] = useState(null);
  const [rates, setRates] = useState([]);
  const [error, setError] = useState("");
  const [form, setForm] = useState({ value: "", tenor: "3M", effective_date: "", source: "" });
  const [submitting, setSubmitting] = useState(false);

  const load = () => {
    benchmarkApi.detail(code).then(({ data }) => setBenchmark(data)).catch(() => setError("Benchmark not found"));
    benchmarkApi.rates(code).then(({ data }) => setRates(data.results || [])).catch(() => setError("Failed to load rates"));
  };

  useEffect(load, [code]);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await benchmarkApi.createRate(code, form);
      addToast("Rate submitted successfully", "success");
      setForm({ value: "", tenor: form.tenor, effective_date: "", source: "" });
      load();
    } catch (err) {
      const msg = err.response?.data?.detail || err.response?.data?.detail?.[0] || "Failed to submit rate";
      addToast(msg, "error");
    } finally {
      setSubmitting(false);
    }
  };

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

      <div className="card">
        <h3>Submit New Rate</h3>
        <form className="rate-form" onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="value">Rate Value</label>
              <input
                id="value"
                name="value"
                type="number"
                step="0.000001"
                value={form.value}
                onChange={handleChange}
                required
                placeholder="e.g. 3.750000"
              />
            </div>
            <div className="form-group">
              <label htmlFor="tenor">Tenor</label>
              <select id="tenor" name="tenor" value={form.tenor} onChange={handleChange}>
                <option value="ON">Overnight</option>
                <option value="1W">1 Week</option>
                <option value="1M">1 Month</option>
                <option value="3M">3 Months</option>
                <option value="6M">6 Months</option>
                <option value="12M">12 Months</option>
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="effective_date">Date</label>
              <input
                id="effective_date"
                name="effective_date"
                type="date"
                value={form.effective_date}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="source">Source</label>
              <input
                id="source"
                name="source"
                value={form.source}
                onChange={handleChange}
                placeholder="e.g. EMMI"
              />
            </div>
          </div>
          <button type="submit" className="btn btn-primary" disabled={submitting}>
            {submitting ? "Submitting..." : "Submit Rate"}
          </button>
        </form>
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
            {rates.map((rate) => (
              <tr key={rate.id}>
                <td>{rate.effective_date}</td>
                <td>{rate.tenor || "-"}</td>
                <td className="mono">{rate.value}</td>
                <td>{rate.source || "-"}</td>
              </tr>
            ))}
            {rates.length === 0 && (
              <tr>
                <td colSpan="4" className="empty-row">No rates recorded yet</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}