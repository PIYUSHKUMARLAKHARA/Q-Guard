import React, { useState } from 'react';
import { Download, RefreshCw, BarChart2, ShieldAlert, Cpu } from 'lucide-react';
import ResultsTable from '../components/ResultsTable';
import FidelityChart from '../components/FidelityChart';
import CorrelationChart from '../components/CorrelationChart';
import { api } from '../services/api';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

export default function Results({ summary, onRefresh }) {
  const experiments = summary?.experiments || [];
  const protectionAnalysis = summary?.protection_analysis || [];
  const [selectedExperiment, setSelectedExperiment] = useState(
    experiments.length > 0 ? experiments[0] : null
  );

  // Filter protected data for acceptance chart
  const acceptanceData = experiments
    .filter((e) => e.protected)
    .map((e) => ({
      processor: e.processor,
      acceptance_rate: parseFloat((e.acceptance_rate * 100).toFixed(1)),
      discarded: e.discarded_shots_avg,
    }));

  // Overhead data
  const overheadData = experiments
    .filter((e) => e.experiment !== 'Ideal')
    .map((e) => ({
      label: `${e.processor} (${e.experiment.includes('Protection') ? 'Prot' : 'Noisy'})`,
      depth: e.average_circuit_depth,
      cx_gates: e.average_two_qubit_gates,
    }));

  return (
    <div className="page-container">
      <div className="page-header" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 className="page-title">Experimental Results & Analytics</h1>
          <p className="page-description">
            Complete empirical dataset calculated from Qiskit Aer simulations. Sort, inspect, and export verified results.
          </p>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem' }}>
          {onRefresh && (
            <button className="btn btn-outline" onClick={onRefresh} title="Reload results from backend">
              <RefreshCw size={15} />
              <span>Refresh</span>
            </button>
          )}
          <a
            href={api.getExportCsvUrl()}
            download="qguard_experiment_results.csv"
            className="btn btn-primary"
            title="Download CSV"
          >
            <Download size={15} />
            <span>Download CSV</span>
          </a>
        </div>
      </div>

      {/* Main Sortable Results Table */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <div className="card-header">
          <h3 className="card-title">All Measured Experiment Runs ({experiments.length})</h3>
          <span className="brand-badge">Click row to inspect correlations</span>
        </div>
        <ResultsTable
          data={experiments}
          selectedId={selectedExperiment?.id}
          onSelectRow={(row) => setSelectedExperiment(row)}
        />
      </div>

      {/* Selected Experiment Correlation Detail */}
      {selectedExperiment && (
        <div className="card" style={{ marginBottom: '2rem' }}>
          <div className="card-header">
            <h3 className="card-title">
              <Cpu size={18} style={{ color: 'var(--accent-cyan)' }} />
              <span>Correlation Breakdown: {selectedExperiment.processor} — {selectedExperiment.experiment}</span>
            </h3>
            <span className="brand-badge">Shots: {selectedExperiment.shots_per_observable}</span>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem', alignItems: 'center' }}>
            <CorrelationChart experiment={selectedExperiment} />
            <div>
              <table className="data-table" style={{ fontSize: '0.85rem' }}>
                <tbody>
                  <tr>
                    <td style={{ color: 'var(--text-muted)' }}>Estimated Fidelity F</td>
                    <td style={{ fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
                      {selectedExperiment.fidelity_estimate.toFixed(5)} ± {(selectedExperiment.fidelity_uncertainty * 2).toFixed(5)}
                    </td>
                  </tr>
                  <tr>
                    <td style={{ color: 'var(--text-muted)' }}>Entanglement Margin (F - 2σ - 0.5)</td>
                    <td style={{ fontFamily: 'var(--font-mono)', color: 'var(--status-success)' }}>
                      +{selectedExperiment.threshold_margin.toFixed(5)}
                    </td>
                  </tr>
                  <tr>
                    <td style={{ color: 'var(--text-muted)' }}>Acceptance Rate</td>
                    <td style={{ fontFamily: 'var(--font-mono)' }}>
                      {(selectedExperiment.acceptance_rate * 100).toFixed(1)}% ({selectedExperiment.accepted_shots_avg} accepted)
                    </td>
                  </tr>
                  <tr>
                    <td style={{ color: 'var(--text-muted)' }}>Circuit Overhead</td>
                    <td style={{ fontFamily: 'var(--font-mono)' }}>
                      Depth {selectedExperiment.average_circuit_depth} | {selectedExperiment.average_two_qubit_gates} CX Gates
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Charts Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(420px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
        {/* Fidelity Chart */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Bell-State Fidelity (F) Comparison</h3>
          </div>
          <FidelityChart data={experiments} />
        </div>

        {/* Acceptance Rate Chart */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Ancilla Postselection Acceptance Rate</h3>
          </div>
          <div style={{ width: '100%', height: 320 }}>
            <ResponsiveContainer>
              <BarChart data={acceptanceData} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#232f4c" />
                <XAxis dataKey="processor" stroke="#94a3b8" />
                <YAxis domain={[0, 105]} unit="%" stroke="#94a3b8" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#111726', borderColor: '#232f4c', borderRadius: '8px', color: '#f1f5f9' }}
                  formatter={(val, name, props) => [`${val}% (Discarded ~${props.payload.discarded} shots)`, 'Acceptance Rate']}
                />
                <Bar dataKey="acceptance_rate" fill="#38bdf8" radius={[4, 4, 0, 0]} name="Acceptance Rate (%)" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Protection Analysis Summary Table */}
      {protectionAnalysis.length > 0 && (
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <ShieldAlert size={18} style={{ color: 'var(--status-warning)' }} />
              <span>NISQ Protection Trade-Off Analysis</span>
            </h3>
            <span className="brand-badge">Scientific Rigor</span>
          </div>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '1rem' }}>
            Comparing the unmitigated noisy baseline vs. ancilla-based postselection.
            Notice that across all three processors, <strong>protected fidelity is lower than noisy baseline</strong> because the gate noise from extra CNOTs (+5 CX gates) outweighs the single-ancilla parity filter.
          </p>
          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Processor</th>
                  <th>Noisy Baseline F</th>
                  <th>Protected F</th>
                  <th>Fidelity Change (ΔF)</th>
                  <th>Acceptance Rate</th>
                  <th>Extra 2Q CX Gates</th>
                  <th>Extra Depth</th>
                  <th>Fidelity Improved?</th>
                </tr>
              </thead>
              <tbody>
                {protectionAnalysis.map((item, idx) => (
                  <tr key={idx}>
                    <td style={{ fontWeight: 600 }}>{item.processor}</td>
                    <td style={{ fontFamily: 'var(--font-mono)' }}>{item.noisy_fidelity?.toFixed(5)}</td>
                    <td style={{ fontFamily: 'var(--font-mono)' }}>{item.protected_fidelity?.toFixed(5)}</td>
                    <td style={{ fontFamily: 'var(--font-mono)', color: item.fidelity_change < 0 ? 'var(--status-danger)' : 'var(--status-success)' }}>
                      {item.fidelity_change > 0 ? '+' : ''}{item.fidelity_change?.toFixed(5)}
                    </td>
                    <td style={{ fontFamily: 'var(--font-mono)' }}>{(item.acceptance_rate * 100).toFixed(1)}%</td>
                    <td style={{ fontFamily: 'var(--font-mono)' }}>+{item.extra_two_qubit_gates}</td>
                    <td style={{ fontFamily: 'var(--font-mono)' }}>+{item.extra_circuit_depth}</td>
                    <td>
                      <span className={item.fidelity_improved ? 'badge badge-pass' : 'badge badge-fail'}>
                        {item.fidelity_improved ? 'YES' : 'NO (NISQ Noise Penalty)'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
