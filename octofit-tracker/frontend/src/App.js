import './App.css';
import logo from './assets/octofitapp-small.svg';
import { NavLink, Routes, Route } from 'react-router-dom';
import Users from './components/Users';
import Teams from './components/Teams';
import Activities from './components/Activities';
import Workouts from './components/Workouts';
import Leaderboard from './components/Leaderboard';

function App() {
  return (
    <div className="container py-3">
      <nav className="navbar navbar-expand-lg navbar-light bg-light mb-3 rounded">
        <div className="container-fluid">
          <span className="navbar-brand d-flex align-items-center">
            <img src={logo} className="brand-logo" alt="OctoFit" />
            <span>OctoFit Tracker</span>
          </span>
          <div className="collapse navbar-collapse">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
              <li className="nav-item"><NavLink className="nav-link" to="/users">Users</NavLink></li>
              <li className="nav-item"><NavLink className="nav-link" to="/teams">Teams</NavLink></li>
              <li className="nav-item"><NavLink className="nav-link" to="/activities">Activities</NavLink></li>
              <li className="nav-item"><NavLink className="nav-link" to="/workouts">Workouts</NavLink></li>
              <li className="nav-item"><NavLink className="nav-link" to="/leaderboards">Leaderboard</NavLink></li>
            </ul>
          </div>
        </div>
      </nav>

      <Routes>
        <Route path="/users" element={<Users />} />
        <Route path="/teams" element={<Teams />} />
        <Route path="/activities" element={<Activities />} />
        <Route path="/workouts" element={<Workouts />} />
        <Route path="/leaderboards" element={<Leaderboard />} />
        <Route path="*" element={<Users />} />
      </Routes>
    </div>
  );
}

export default App;
