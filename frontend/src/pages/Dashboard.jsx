import React from 'react';
import { Activity, ShieldCheck, Cpu, ArrowUpRight, Play, AlertTriangle, Layers, Percent } from 'lucide-react';
import MetricCard from '../components/MetricCard';
import FidelityChart from '../components/FidelityChart';
import ResultsTable from '../components/ResultsTable';

export default function Dashboard({ summary, processors, onNavigate, onSelectExperiment }) {
  const experiments = summary?.experiments || [];
  const latestRun = experiments.length > 0 ? experiments[experiments.length - 1] : null;

  // Compute key stats
  const totalRuns = experiments.length;
  const avgFidelity =
    experiments.length > 0
      ? (experiments.reduce((acc, curr) => acc + curr.fidelity_estimate, 0) / experiments.length).toFixed(4)
      : '0.0000';
  const thresholdPassRate =
    experiments.length > 0
      ? (
          (experiments.filter((e) => e.threshold_passed).length / experiments.length) *
          100
        ).toFixed(1)
      : '0.0';

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Quantum Protection Dashboard</h1>
        <p className="page-description">
          Real-time NISQ simulation benchmark evaluating Bell state $|\\Phi^+\\rangle$ preparation,
          ancilla-assisted $ZZ$ parity postselection, and physical decoherence across realistic processor topologies.
        </p>
      </div>

      <div className="alert-banner">
        <AlertTriangle size={20} style={{ flexShrink: 0 }} />
        <div>
          <strong>Illustrative Device Notice:</strong> Processor parameters (2016-Inspired, Contemporary, Hyperbolic-Inspired)
          are illustrative topology presets. Simulations run on real Qiskit Aer density matrix engines.
        </div>
      </div>

      {/* Metrics Row */}
      <div className="metric-grid">
        <MetricCard
          label="Available Topologies"
          value={processors?.length || 3}
          subtext="5Q, 7Q, and 9Q coupling layouts"
          icon={Cpu}
          color="cyan"
          tooltip="Physical chip topologies configured in config/processors.json"
        />
        <MetricCard
          label="Latest Fidelity (F)"
          value={latestRun ? latestRun.fidelity_estimate.toFixed(5) : 'N/A'}
          subtext={latestRun ? `±${(latestRun.fidelity_uncertainty * 2).toFixed(5)} (95% CI)` : 'No runs yet'}
          icon={Activity}
          color="blue"
          tooltip="Bell state fidelity estimated from signed XX, YY, and ZZ correlations"
        />
        <MetricCard
          label="Entanglement Witness"
          value={`${thresholdPassRate}%`}
          subtext="Passed F - 2σ > 0.5 criterion"
          icon={ShieldCheck}
          color="violet"
          tooltip="Statistically verified non-classical entanglement witness threshold"
        />
        <MetricCard
          label="Total Experiments"
          value={totalRuns}
          subtext="Recorded across all profiles"
          icon={Layers}
          color="purple"
        />
      </div>

      {/* Charts & Latest Run Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(420px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Fidelity Comparison Across Processors</h3>
            <span className="brand-badge">Ideal vs. Noisy vs. Protected</span>
          </div>
          <FidelityChart data={experiments} />
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Quick Simulation Control</h3>
          </div>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem', marginBottom: '1.25rem' }}>
            Run customized quantum experiments on Qiskit Aer, or execute the full 3x3 benchmark matrix.
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <button
              className="btn btn-primary"
              style={{ justifyContent: 'flex-start', padding: '0.85rem 1.25rem' }}
              onClick={() => onNavigate('experiments')}
            >
              <Play size={18} />
              <span>Launch Single Experiment Form</span>
              <ArrowUpRight size={16} style={{ marginLeft: 'auto' }} />
            </button>
            <button
              className="btn btn-secondary"
              style={{ justifyContent: 'flex-start', padding: '0.85rem 1.25rem' }}
              onClick={() => onNavigate('results')}
            >
              <Activity size={18} />
              <span>Explore Analytical Results & Charts</span>
              <ArrowUpRight size={16} style={{ marginLeft: 'auto' }} />
            </button>
            <button
              className="btn btn-outline"
              style={{ justifyContent: 'flex-start', padding: '0.85rem 1.25rem' }}
              onClick={() => onNavigate('methodology')}
            >
              <Cpu size={18} />
              <span>Read Mathematical Methodology</span>
              <ArrowUpRight size={16} style={{ marginLeft: 'auto' }} />
            </button>
          </div>
        </div>
      </div>

      {/* Recent Experiments Table */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Recent Experiment Runs</h3>
          <button className="btn btn-outline" style={{ fontSize: '0.82rem', padding: '0.4rem 0.8rem' }} onClick={() => onNavigate('results')}>
            View All ({experiments.length})
          </button>
        </div>
        <ResultsTable
          data={experiments.slice(-6).reverse()}
          onSelectRow={(row) => {
            onSelectExperiment && onSelectExperiment(row);
            onNavigate('results');
          }}
        />
      </div>
    </div>
  );
}
