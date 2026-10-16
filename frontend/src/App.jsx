import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Experiments from './pages/Experiments';
import Results from './pages/Results';
import Methodology from './pages/Methodology';
import About from './pages/About';
import LoadingState from './components/LoadingState';
import { api } from './services/api';

export default function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [summary, setSummary] = useState(null);
  const [processors, setProcessors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [apiError, setApiError] = useState(null);
  const [theme, setTheme] = useState('dark');

  const loadInitialData = async () => {
    setLoading(true);
    setApiError(null);
    try {
      const [procs, sum] = await Promise.all([
        api.getProcessors(),
        api.getSummary(),
      ]);
      setProcessors(procs);
      setSummary(sum);
    } catch (err) {
      console.error('Failed to load initial data:', err);
      setApiError(
        'Backend connection failed. Ensure FastAPI is running on http://127.0.0.1:8000.'
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadInitialData();
  }, []);

  const handleExperimentComplete = async () => {
    try {
      const updatedSummary = await api.getSummary();
      setSummary(updatedSummary);
    } catch (err) {
      console.error('Failed to refresh summary:', err);
    }
  };

  const toggleTheme = () => {
    const nextTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(nextTheme);
    document.documentElement.setAttribute('data-theme', nextTheme);
  };

  return (
    <div className="app-layout">
      <Sidebar currentPage={currentPage} onNavigate={setCurrentPage} />

      <div className="main-content">
        <Navbar
          theme={theme}
          onToggleTheme={toggleTheme}
          onNavigate={setCurrentPage}
        />

        {apiError && (
          <div style={{ margin: '1.5rem 2.5rem 0 2.5rem', padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '8px', color: '#f87171', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span>{apiError}</span>
            <button className="btn btn-outline" style={{ fontSize: '0.8rem', padding: '0.35rem 0.75rem' }} onClick={loadInitialData}>
              Retry Connection
            </button>
          </div>
        )}

        {loading ? (
          <div className="page-container">
            <LoadingState message="Connecting to Q-Guard backend and Qiskit engine..." />
          </div>
        ) : (
          <>
            {currentPage === 'dashboard' && (
              <Dashboard
                summary={summary}
                processors={processors}
                onNavigate={setCurrentPage}
              />
            )}
            {currentPage === 'experiments' && (
              <Experiments
                processors={processors}
                onExperimentComplete={handleExperimentComplete}
              />
            )}
            {currentPage === 'results' && (
              <Results
                summary={summary}
                onRefresh={loadInitialData}
              />
            )}
            {currentPage === 'methodology' && <Methodology />}
            {currentPage === 'about' && <About />}
          </>
        )}
      </div>
    </div>
  );
}
