import React, { useEffect, useMemo, useState } from 'react';

const Users = () => {
  const [items, setItems] = useState([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selected, setSelected] = useState(null);

  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  const url = codespace ? `https://${codespace}-8000.app.github.dev/api/users/` : 'http://localhost:8000/api/users/';

  const load = () => {
    setLoading(true);
    setError(null);
    console.log('Users endpoint:', url);
    fetch(url)
      .then(res => res.json())
      .then(data => {
        console.log('Users data:', data);
        const list = Array.isArray(data) ? data : (data.results || []);
        setItems(list);
      })
      .catch(err => {
        console.error('Users fetch error:', err);
        setError('Failed to load users');
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, [url]);

  const filtered = useMemo(() => {
    const q = query.toLowerCase();
    return items.filter(u =>
      (u.username || '').toLowerCase().includes(q) ||
      (u.email || '').toLowerCase().includes(q)
    );
  }, [items, query]);

  return (
    <div className="card shadow-sm">
      <div className="card-header d-flex justify-content-between align-items-center">
        <h2 className="h5 mb-0">Users</h2>
        <div className="d-flex gap-2">
          <button className="btn btn-outline-secondary btn-sm" onClick={load}>Refresh</button>
        </div>
      </div>
      <div className="card-body">
        <form className="row g-2 mb-3" onSubmit={e => e.preventDefault()}>
          <div className="col-auto">
            <input className="form-control" placeholder="Search users..." value={query} onChange={e => setQuery(e.target.value)} />
          </div>
        </form>
        {loading && <div className="alert alert-info">Loading...</div>}
        {error && <div className="alert alert-danger">{error}</div>}
        <div className="table-responsive">
          <table className="table table-striped table-hover align-middle">
            <thead>
              <tr>
                <th>Username</th>
                <th>Email</th>
                <th>Team</th>
                <th style={{width: 120}}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map(u => (
                <tr key={u.id || u._id || u.username}>
                  <td>{u.username}</td>
                  <td><a className="link-primary" href={`mailto:${u.email}`}>{u.email}</a></td>
                  <td>{u.team?.name || u.team || '-'}</td>
                  <td>
                    <button
                      type="button"
                      className="btn btn-sm btn-primary"
                      data-bs-toggle="modal"
                      data-bs-target="#usersModal"
                      onClick={() => setSelected(u)}
                    >View</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="modal fade" id="usersModal" tabIndex="-1" aria-hidden="true">
        <div className="modal-dialog modal-dialog-centered modal-lg">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">User Details</h5>
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

export default Users;
