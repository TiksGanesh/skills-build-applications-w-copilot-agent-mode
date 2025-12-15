import React, { useEffect, useMemo, useState } from 'react';

const Activities = () => {
  const [items, setItems] = useState([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selected, setSelected] = useState(null);

  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  const base = codespace ? `https://${codespace}-8000.app.github.dev` : 'http://localhost:8000';
  const url = `${base}/api/activities/`;

  const load = () => {
    setLoading(true);
    setError(null);
    console.log('Activities endpoint:', url);
    fetch(url)
      .then(res => res.json())
      .then(data => {
        console.log('Activities data:', data);
        const list = Array.isArray(data) ? data : (data.results || []);
        setItems(list);
      })
      .catch(err => { console.error('Activities fetch error:', err); setError('Failed to load activities'); })
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, [url]);

  const filtered = useMemo(() => {
    const q = query.toLowerCase();
    return items.filter(a =>
      (a.type || '').toLowerCase().includes(q) ||
      String(a.duration || '').includes(q) ||
      String(a.distance || '').includes(q)
    );
  }, [items, query]);

  return (
    <div className="card shadow-sm">
      <div className="card-header d-flex justify-content-between align-items-center">
        <h2 className="h5 mb-0">Activities</h2>
        <button className="btn btn-outline-secondary btn-sm" onClick={load}>Refresh</button>
      </div>
      <div className="card-body">
        <form className="row g-2 mb-3" onSubmit={e => e.preventDefault()}>
          <div className="col-auto">
            <input className="form-control" placeholder="Search activities..." value={query} onChange={e => setQuery(e.target.value)} />
          </div>
        </form>
        {loading && <div className="alert alert-info">Loading...</div>}
        {error && <div className="alert alert-danger">{error}</div>}
        <div className="table-responsive">
          <table className="table table-striped table-hover align-middle">
            <thead>
              <tr>
                <th>Type</th>
                <th>Duration (m)</th>
                <th>Distance (km)</th>
                <th style={{width:120}}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((a, idx) => (
                <tr key={a.id || a._id || idx}>
                  <td>{a.type}</td>
                  <td>{a.duration}</td>
                  <td>{a.distance}</td>
                  <td>
                    <button type="button" className="btn btn-sm btn-primary" data-bs-toggle="modal" data-bs-target="#activitiesModal" onClick={() => setSelected(a)}>View</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="modal fade" id="activitiesModal" tabIndex="-1" aria-hidden="true">
        <div className="modal-dialog modal-dialog-centered">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">Activity Details</h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div className="modal-body">
              <pre className="bg-light p-3 rounded small mb-0">{selected ? JSON.stringify(selected, null, 2) : 'No selection'}</pre>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Activities;
