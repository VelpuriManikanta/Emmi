import { useEffect, useState } from "react";
import { reportApi, benchmarkApi } from "../api";
import { useToast } from "../context/ToastContext";
import "../styles.css";

export default function Reports() {
  const { addToast } = useToast();
  const [reports, setReports] = useState([]);
  const [benchmarks, setBenchmarks] = useState([]);
  const [error, setError] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [creating, setCreating] = useState(false);
  const [form, setForm] = useState({
    title: "",
    report_type: "DAILY",
    start_date: "",
    end_date: "",
    benchmark_ids: [],
  });

  const load = () => {
    reportApi.list().then(({ data }) => setReports(data.results || [])).catch(() => setError("Failed to load reports"));
    benchmarkApi.list().then(({ data }) => setBenchmarks(data.results || [])).catch(() => {});
  };

  useEffect(load, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const handleBenchToggle = (id) => {
    setForm((prev) => ({
      ...prev,
      benchmark_ids: prev.benchmark_ids.includes(id)
        ? prev.benchmark_ids.filter((b) => b !== id)
        : [...prev.benchmark_ids, id],
    }));
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setCreating(true);
    try {
      await reportApi.create(form);
      addToast("Report created", "success");
      setShowModal(false);
      setForm({ title: "", report_type: "DAILY", start_date: "", end_date: "", benchmark_ids: [] });
      load();
    } catch (err) {
      addToast("Failed to create report", "error");
    } finally {
      setCreating(false);
    }
  };

  const handleGenerate = async (id) => {
    try {
      await reportApi.generate(id);
      addToast("Report generated", "success");
      load();
    } catch {
      addToast("Generation failed", "error");
    }
  };

  const handleExport = async (id, title) => {
    try {
      const { data } = await reportApi.export(id);
      const url = window.URL.createObjectURL(data);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${title}.csv`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch {
      addToast("Export failed", "error");
    }
  };

  if (error) return <div className="alert alert-error">{error}</div>;

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Reports</h1>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          + New Report
        </button>
      </div>

      <div className="table-wrap">
        <table className="data-table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Type</th>
              <th>Status</th>
              <th>Period</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {reports.map((r) => (
              <tr key={r.id}>
                <td>{r.title}</td>
                <td>{r.report_type}</td>
                <td>
                  <span className={`badge badge-${r.status.toLowerCase()}`}>{r.status}</span>
                </td>
                <td>
                  {r.start_date} → {r.end_date}
                </td>
                <td className="actions-cell">
                  <button className="btn btn-small" onClick={() => handleGenerate(r.id)}>Generate</button>
                  <button className="btn btn-small" onClick={() => handleExport(r.id, r.title)}>Export</button>
                </td>
              </tr>
            ))}
            {reports.length === 0 && (
              <tr>
                <td colSpan="5" className="empty-row">No reports yet — create one above</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {showModal && (
        <div className="modal-backdrop" onClick={() => setShowModal(false)}>
          <div className="modal-card" onClick={(e) => e.stopPropagation()}>
            <h2>Create Report</h2>
            <form onSubmit={handleCreate}>
              <label htmlFor="title">Title</label>
              <input
                id="title"
                name="title"
                value={form.title}
                onChange={handleChange}
                required
                placeholder="e.g. Daily EURIBOR Summary"
              />

              <label htmlFor="report_type">Report Type</label>
              <select id="report_type" name="report_type" value={form.report_type} onChange={handleChange}>
                <option value="DAILY">Daily</option>
                <option value="WEEKLY">Weekly</option>
                <option value="MONTHLY">Monthly</option>
                <option value="CUSTOM">Custom</option>
              </select>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="start_date">Start Date</label>
                  <input
                    id="start_date"
                    name="start_date"
                    type="date"
                    value={form.start_date}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="end_date">End Date</label>
                  <input
                    id="end_date"
                    name="end_date"
                    type="date"
                    value={form.end_date}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>

              <fieldset className="checkbox-group">
                <legend>Benchmarks (leave empty = all active)</legend>
                {benchmarks.map((b) => (
                  <label key={b.code} className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={form.benchmark_ids.includes(b.id)}
                      onChange={() => handleBenchToggle(b.id)}
                    />
                    {b.code}
                  </label>
                ))}
              </fieldset>

              <div className="modal-actions">
                <button type="button" className="btn btn-ghost-dark" onClick={() => setShowModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary" disabled={creating}>
                  {creating ? "Creating..." : "Create Report"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}