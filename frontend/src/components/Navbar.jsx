import React from 'react';
import { Sun, Moon, Download, Play } from 'lucide-react';
import { api } from '../services/api';

export default function Navbar({ theme, onToggleTheme, onNavigate }) {
  return (
    <header className="top-navbar">
      <div className="top-navbar-title">
        Quantum Error Detection & Protection Optimizer
      </div>
      <div className="top-navbar-actions">
        <a
          href={api.getExportCsvUrl()}
          download="qguard_experiment_results.csv"
          className="btn btn-outline"
          style={{ padding: '0.45rem 0.85rem', fontSize: '0.82rem' }}
          title="Download raw experiment results as CSV"
        >
          <Download size={15} />
          <span>Export CSV</span>
        </a>

        <button
          className="btn btn-primary"
          style={{ padding: '0.45rem 1rem', fontSize: '0.85rem' }}
          onClick={() => onNavigate('experiments')}
        >
          <Play size={15} />
          <span>New Run</span>
        </button>

        {onToggleTheme && (
          <button
            className="btn btn-outline"
            style={{ padding: '0.5rem', borderRadius: '50%' }}
            onClick={onToggleTheme}
            title="Toggle theme"
          >
            {theme === 'dark' ? <Sun size={16} /> : <Moon size={16} />}
          </button>
        )}
      </div>
    </header>
  );
}
