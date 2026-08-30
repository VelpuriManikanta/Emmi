import { useEffect, useState } from "react";
import { reportApi } from "../api";
import "../styles.css";

export default function Reports() {
  const [reports, setReports] = useState([]);
  const [error, setError] = useState("");

  const load = () => {
    reportApi
      .list()
      .then(({ data }) => setReports(data.results || []))
      .catch(() => setError("Failed to load reports"));
  };

  useEffect(load, []);

  const handleGenerate = async (id) => {
    await reportApi.generate(id);
    load();
  };

  const handleExport = async (id, title) => {
    const { data } = await reportApi.export(id);
    const url = window.URL.createObjectURL(data);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${title}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  if (error) return <div className="alert alert-error">{error}</div>;

  return (
    <div>
      <h1 className="page-title">Reports</h1>

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
                <td>
                  <button className="btn btn-small" onClick={() => handleGenerate(r.id)}>
                    Generate
                  </button>{" "}
                  <button className="btn btn-small" onClick={() => handleExport(r.id, r.title)}>
                    Export
                  </button>
                </td>
              </tr>
            ))}
            {reports.length === 0 && (
              <tr>
                <td colSpan="5" className="empty-row">
                  No reports yet
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}