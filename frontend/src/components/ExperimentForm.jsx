import React, { useState } from 'react';
import { Play, Sparkles, Layers, Sliders, Hash } from 'lucide-react';

export default function ExperimentForm({ processors, onSubmit, isRunning }) {
  const [processorId, setProcessorId] = useState(
    processors && processors.length > 0 ? processors[0].id : 'contemporary'
  );
  const [experimentType, setExperimentType] = useState('Noisy + Protection');
  const [shots, setShots] = useState(4096);
  const [seed, setSeed] = useState(42);
  const [observable, setObservable] = useState('ALL');
  const [error, setError] = useState(null);

  const selectedProcessor = processors?.find((p) => p.id === processorId) || processors?.[0];

  const handleSubmit = (e) => {
    e.preventDefault();
    setError(null);

    if (shots < 100 || shots > 20000) {
      setError('Shots must be between 100 and 20,000.');
      return;
    }

    if (seed < 0) {
      setError('Seed must be a non-negative integer.');
      return;
    }

    onSubmit({
      processor_id: processorId,
      experiment_type: experimentType,
      shots: parseInt(shots, 10),
      seed: parseInt(seed, 10),
      observable: observable,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="card">
      <div className="card-header">
        <h3 className="card-title">
          <Sliders size={18} style={{ color: 'var(--accent-cyan)' }} />
          <span>Experiment Configuration</span>
        </h3>
        <span className="brand-badge">Real Qiskit Aer</span>
      </div>

      {error && (
        <div style={{ color: 'var(--status-danger)', marginBottom: '1rem', fontSize: '0.88rem' }}>
          {error}
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.25rem' }}>
        {/* Processor Selection */}
        <div className="form-group">
          <label className="form-label">Target Processor Topology</label>
          <select
            className="form-select"
            value={processorId}
            onChange={(e) => setProcessorId(e.target.value)}
            disabled={isRunning}
          >
            {processors?.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name} ({p.qubits} Qubits)
              </option>
            ))}
          </select>
          {selectedProcessor && (
            <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '0.4rem' }}>
              Error Rates: 1Q {selectedProcessor.single_qubit_depolarizing * 100}% | 2Q {selectedProcessor.two_qubit_depolarizing * 100}% | Readout {selectedProcessor.readout_error * 100}%
            </div>
          )}
        </div>

        {/* Experiment Type */}
        <div className="form-group">
          <label className="form-label">Simulation Condition</label>
          <select
            className="form-select"
            value={experimentType}
            onChange={(e) => setExperimentType(e.target.value)}
            disabled={isRunning}
          >
            <option value="Ideal">Ideal Reference (No physical noise)</option>
            <option value="Noisy">Noisy Baseline (Physical depolarizing & readout)</option>
            <option value="Noisy + Protection">Noisy + Ancilla Parity Protection</option>
          </select>
          <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '0.4rem' }}>
            {experimentType === 'Noisy + Protection'
              ? 'Measures ZZ parity on ancilla qa, accepts only qa = 0 shots.'
              : experimentType === 'Ideal'
              ? 'Perfect gates and measurements without noise.'
              : 'Applies realistic physical noise without error protection.'}
          </div>
        </div>

        {/* Shots */}
        <div className="form-group">
          <label className="form-label">Shots per Observable (100 - 20,000)</label>
          <input
            type="number"
            className="form-input"
            value={shots}
            onChange={(e) => setShots(e.target.value)}
            min={100}
            max={20000}
            step={128}
            disabled={isRunning}
          />
          <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '0.4rem' }}>
            Default: 4,096 shots for high statistical precision.
          </div>
        </div>

        {/* Seed */}
        <div className="form-group">
          <label className="form-label">Simulation Seed (Deterministic)</label>
          <input
            type="number"
            className="form-input"
            value={seed}
            onChange={(e) => setSeed(e.target.value)}
            min={0}
            disabled={isRunning}
          />
          <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '0.4rem' }}>
            Seed guarantees exact reproducibility of measurements.
          </div>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid var(--border-color)' }}>
        <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
          * Executes real Qiskit circuit transpilation and noisy density matrix simulation.
        </div>
        <button type="submit" className="btn btn-primary" disabled={isRunning}>
          {isRunning ? (
            <>
              <div className="spinner" style={{ width: 16, height: 16, margin: 0, borderWidth: 2 }} />
              <span>Simulating...</span>
            </>
          ) : (
            <>
              <Play size={16} />
              <span>Run Experiment</span>
            </>
          )}
        </button>
      </div>
    </form>
  );
}
