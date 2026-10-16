import React, { useState } from 'react';
import { Play, Layers, CheckCircle2, XCircle, AlertCircle, Sparkles } from 'lucide-react';
import ExperimentForm from '../components/ExperimentForm';
import LoadingState from '../components/LoadingState';
import CorrelationChart from '../components/CorrelationChart';
import { api } from '../services/api';

export default function Experiments({ processors, onExperimentComplete }) {
  const [isRunning, setIsRunning] = useState(false);
  const [isBatchRunning, setIsBatchRunning] = useState(false);
  const [latestResult, setLatestResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  const handleRunSingle = async (payload) => {
    setIsRunning(true);
    setErrorMessage(null);
    setSuccessMessage(null);
    try {
      const res = await api.runExperiment(payload);
      setLatestResult(res);
      setSuccessMessage(
        `Experiment on ${res.processor} (${res.experiment}) completed successfully with fidelity F = ${res.fidelity_estimate.toFixed(5)}!`
      );
      if (onExperimentComplete) onExperimentComplete(res);
    } catch (err) {
      setErrorMessage(err.message || 'Simulation failed to execute.');
    } finally {
      setIsRunning(false);
    }
  };

  const handleRunBatch = async () => {
    setIsBatchRunning(true);
    setErrorMessage(null);
    setSuccessMessage(null);
    try {
      const results = await api.runAllExperiments();
      setLatestResult(results[results.length - 1]);
      setSuccessMessage(`Successfully executed full 3x3 experimental matrix (9 runs total)!`);
      if (onExperimentComplete) onExperimentComplete(results);
    } catch (err) {
      setErrorMessage(err.message || 'Batch simulation failed.');
    } finally {
      setIsBatchRunning(false);
    }
  };

  return (
    <div className="page-container">
      <div className="page-header" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 className="page-title">Run Quantum Experiments</h1>
          <p className="page-description">
            Configure target processor topology, physical noise channels, and ancilla parity postselection.
          </p>
        </div>

        <button
          className="btn btn-secondary"
          onClick={handleRunBatch}
          disabled={isRunning || isBatchRunning}
          title="Run all 3 processors across Ideal, Noisy, and Protected cases"
        >
          {isBatchRunning ? (
            <>
              <div className="spinner" style={{ width: 14, height: 14, margin: 0, borderWidth: 2 }} />
              <span>Simulating Full Matrix (3x3)...</span>
            </>
          ) : (
            <>
              <Layers size={16} />
              <span>Run Full 3x3 Matrix</span>
            </>
          )}
        </button>
      </div>

      {successMessage && (
        <div style={{ background: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.3)', color: '#34d399', padding: '0.85rem 1.25rem', borderRadius: '8px', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <CheckCircle2 size={18} />
          <span>{successMessage}</span>
        </div>
      )}

      {errorMessage && (
        <div style={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', color: '#f87171', padding: '0.85rem 1.25rem', borderRadius: '8px', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <AlertCircle size={18} />
          <span>{errorMessage}</span>
        </div>
      )}

      {/* Main Configuration Form */}
      <ExperimentForm
        processors={processors}
        onSubmit={handleRunSingle}
        isRunning={isRunning || isBatchRunning}
      />

      {/* Live Simulation Loading Indicator */}
      {(isRunning || isBatchRunning) && (
        <div style={{ marginTop: '1.5rem' }}>
          <LoadingState message={isBatchRunning ? 'Executing 3x3 multi-processor matrix...' : 'Simulating quantum circuit on Qiskit Aer...'} />
        </div>
      )}

      {/* Latest Execution Breakdown */}
      {latestResult && !isRunning && !isBatchRunning && (
        <div className="card" style={{ marginTop: '2rem' }}>
          <div className="card-header">
            <h3 className="card-title">
              <Sparkles size={18} style={{ color: 'var(--accent-cyan)' }} />
              <span>Latest Execution Result: {latestResult.processor} ({latestResult.experiment})</span>
            </h3>
            <span className={latestResult.threshold_passed ? 'badge badge-pass' : 'badge badge-fail'}>
              {latestResult.threshold_passed ? 'PASS: Entanglement Witness' : 'FAIL: Classical Limit'}
            </span>
          </div>

          <div className="metric-grid" style={{ marginBottom: '1.5rem' }}>
            <div className="metric-card">
              <span className="metric-label">Estimated Fidelity</span>
              <div className="metric-value">{latestResult.fidelity_estimate.toFixed(5)}</div>
              <div className="metric-sub">±{(latestResult.fidelity_uncertainty * 2).toFixed(5)} (2σ)</div>
            </div>
            <div className="metric-card">
              <span className="metric-label">F - 2σ Margin</span>
              <div className="metric-value">{latestResult.f_minus_2sigma.toFixed(5)}</div>
              <div className="metric-sub">Margin over 0.5: +{latestResult.threshold_margin.toFixed(5)}</div>
            </div>
            <div className="metric-card">
              <span className="metric-label">Acceptance Rate</span>
              <div className="metric-value">{(latestResult.acceptance_rate * 100).toFixed(1)}%</div>
              <div className="metric-sub">{latestResult.accepted_shots_avg} / {latestResult.total_shots_avg} shots</div>
            </div>
            <div className="metric-card">
              <span className="metric-label">Circuit Resources</span>
              <div className="metric-value">Depth {latestResult.average_circuit_depth}</div>
              <div className="metric-sub">{latestResult.average_two_qubit_gates} CX Gates | {latestResult.average_one_qubit_gates} 1Q Gates</div>
            </div>
          </div>

          <div>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 600, marginBottom: '0.75rem', color: 'var(--text-secondary)' }}>
              Pauli Correlation Measurements (⟨XX⟩, ⟨YY⟩, ⟨ZZ⟩)
            </h4>
            <CorrelationChart experiment={latestResult} />
          </div>
        </div>
      )}
    </div>
  );
}
