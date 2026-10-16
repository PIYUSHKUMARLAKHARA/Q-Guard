import React from 'react';
import { Info, Code, FileText, CheckCircle2, AlertTriangle, ShieldCheck } from 'lucide-react';

export default function About() {
  const stack = [
    { name: 'Quantum Simulator', tech: 'Qiskit 2.5.2 & Qiskit Aer 0.17.2' },
    { name: 'Backend API', tech: 'Python 3.12, FastAPI, Uvicorn, Pydantic' },
    { name: 'Frontend Dashboard', tech: 'React 18, Vite 5, Recharts, Lucide Icons' },
    { name: 'Data & Analytics', tech: 'Pandas 3.0, NumPy 2.5, Matplotlib 3.11' },
    { name: 'Testing Framework', tech: 'Python unittest (66 Automated Unit & API Tests)' },
  ];

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">About Q-Guard</h1>
        <p className="page-description">
          Quantum Error Detection and Protection Optimizer — Hackathon Basic Track.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(380px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <Info size={18} style={{ color: 'var(--accent-cyan)' }} />
              <span>Project Mission</span>
            </h3>
            <span className="brand-badge">Basic Track</span>
          </div>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem', lineHeight: '1.6', marginBottom: '1rem' }}>
            Q-Guard is an educational and benchmarking quantum simulation framework designed to explore the boundary between NISQ gate noise and error detection. It models realistic processor topologies and provides empirical evidence for the overhead trade-offs of ancilla-assisted postselection.
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.88rem' }}>
              <CheckCircle2 size={16} style={{ color: 'var(--status-success)' }} />
              <span>Bell State Preparation & Multi-Basis Pauli Tomography</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.88rem' }}>
              <CheckCircle2 size={16} style={{ color: 'var(--status-success)' }} />
              <span>Depolarizing & Readout Noise Simulation on Qiskit Aer</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.88rem' }}>
              <CheckCircle2 size={16} style={{ color: 'var(--status-success)' }} />
              <span>Rigorous Statistical Uncertainty (Gaussian Error Propagation)</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.88rem' }}>
              <CheckCircle2 size={16} style={{ color: 'var(--status-success)' }} />
              <span>Entanglement Certification (F - 2σ &gt; 0.50 Decision Rule)</span>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <Code size={18} style={{ color: 'var(--accent-violet)' }} />
              <span>Technology Stack</span>
            </h3>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {stack.map((item, idx) => (
              <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', padding: '0.65rem', background: 'var(--bg-tertiary)', borderRadius: '6px', fontSize: '0.88rem' }}>
                <span style={{ color: 'var(--text-muted)' }}>{item.name}</span>
                <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 600 }}>{item.tech}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Disclaimers & Limitations */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <div className="card-header">
          <h3 className="card-title">
            <AlertTriangle size={18} style={{ color: '#fbbf24' }} />
            <span>Important Scientific Disclaimers</span>
          </h3>
        </div>
        <ul style={{ paddingLeft: '1.25rem', color: 'var(--text-secondary)', fontSize: '0.92rem', display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
          <li>
            <strong>Illustrative Hardware Parameters:</strong> Processor specifications (qubit numbers, coupling graphs, and depolarizing error rates) are illustrative benchmarks designed to test topologies; they do not represent real calibrated IBM Quantum, Google Quantum AI, or Rigetti hardware runs.
          </li>
          <li>
            <strong>Simulator vs. Real Hardware:</strong> All experimental findings are generated via numerical density matrix simulation using Qiskit Aer.
          </li>
          <li>
            <strong>Selective Parity Check:</strong> The implemented circuit is an error-detecting postselection filter, not a fault-tolerant quantum error-correcting code (QECC).
          </li>
          <li>
            <strong>Scientific Honesty:</strong> Protected fidelity is lower than unmitigated noisy baseline due to the gate error overhead of additional CNOT operations in NISQ systems.
          </li>
        </ul>
      </div>

      {/* Documentation Files */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">
            <FileText size={18} style={{ color: 'var(--accent-blue)' }} />
            <span>Project Documentation Artifacts</span>
          </h3>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1rem' }}>
          <div style={{ padding: '1rem', background: 'var(--bg-tertiary)', borderRadius: '8px' }}>
            <div style={{ fontWeight: 600, color: 'var(--accent-cyan)' }}>docs/REQUIREMENTS_AUDIT.md</div>
            <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
              Detailed Hackathon Basic Track compliance checklist.
            </div>
          </div>
          <div style={{ padding: '1rem', background: 'var(--bg-tertiary)', borderRadius: '8px' }}>
            <div style={{ fontWeight: 600, color: 'var(--accent-cyan)' }}>docs/LIMITATIONS.md</div>
            <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
              In-depth analysis of NISQ gate overhead & error selectivity.
            </div>
          </div>
          <div style={{ padding: '1rem', background: 'var(--bg-tertiary)', borderRadius: '8px' }}>
            <div style={{ fontWeight: 600, color: 'var(--accent-cyan)' }}>docs/METHODOLOGY.md</div>
            <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
              Mathematical formulation of Pauli rotations & uncertainty propagation.
            </div>
          </div>
          <div style={{ padding: '1rem', background: 'var(--bg-tertiary)', borderRadius: '8px' }}>
            <div style={{ fontWeight: 600, color: 'var(--accent-cyan)' }}>docs/RUN_WEBSITE.md</div>
            <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
              Beginner-friendly guide to run both backend and frontend locally.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
