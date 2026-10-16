import React from 'react';
import { LayoutDashboard, PlayCircle, BarChart3, BookOpen, Info, Cpu } from 'lucide-react';

export default function Sidebar({ currentPage, onNavigate }) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'experiments', label: 'Run Experiment', icon: PlayCircle },
    { id: 'results', label: 'Results & Charts', icon: BarChart3 },
    { id: 'methodology', label: 'Methodology', icon: BookOpen },
    { id: 'about', label: 'About & Specs', icon: Info },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="brand-icon">
          <Cpu size={20} />
        </div>
        <div>
          <h1 className="brand-title">Q-Guard</h1>
        </div>
        <span className="brand-badge">NISQ</span>
      </div>

      <nav>
        <ul className="nav-list">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentPage === item.id;
            return (
              <li key={item.id}>
                <button
                  type="button"
                  className={`nav-item ${isActive ? 'active' : ''}`}
                  onClick={() => onNavigate(item.id)}
                  style={{ width: '100%', border: 'none', background: 'transparent', textAlign: 'left' }}
                >
                  <Icon size={18} />
                  <span>{item.label}</span>
                </button>
              </li>
            );
          })}
        </ul>
      </nav>

      <div className="sidebar-footer">
        <div style={{ marginBottom: '0.5rem' }}>Simulator Status:</div>
        <div className="status-pill">
          <span className="status-dot"></span>
          <span>Qiskit Aer Ready</span>
        </div>
      </div>
    </aside>
  );
}
