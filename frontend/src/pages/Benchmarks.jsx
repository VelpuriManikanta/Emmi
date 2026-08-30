import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { benchmarkApi } from "../api";
import "../styles.css";

export default function Benchmarks() {
  const [benchmarks, setBenchmarks] = useState([]);
  const [search, setSearch] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    benchmarkApi
      .list({ search: search || undefined })
      .then(({ data }) => setBenchmarks(data.results || []))
      .catch(() => setError("Failed to load benchmarks"));
  }, [search]);

  if (error) return <div className="alert alert-error">{error}</div>;

  return (
    <div>
      <h1 className="page-title">Benchmarks</h1>

      <input
        type="text"
        placeholder="Search benchmarks..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="search-input"
      />

      <div className="table-wrap">
        <table className="data-table">
          <thead>
            <tr>
              <th>Code</th>
              <th>Name</th>
              <th>Type</th>
              <th>Currency</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {benchmarks.map((b) => (
              <tr key={b.code}>
                <td>
                  <Link to={`/benchmarks/${b.code}`}>{b.code}</Link>
                </td>
                <td>{b.name}</td>
                <td>{b.benchmark_type?.name || "-"}</td>
                <td>{b.currency}</td>
                <td>
                  <span className={`badge ${b.is_active ? "badge-active" : "badge-inactive"}`}>
                    {b.is_active ? "Active" : "Inactive"}
                  </span>
                </td>
              </tr>
            ))}
            {benchmarks.length === 0 && (
              <tr>
                <td colSpan="5" className="empty-row">
                  No benchmarks found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}