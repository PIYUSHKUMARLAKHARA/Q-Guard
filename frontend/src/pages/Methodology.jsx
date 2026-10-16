import React from 'react';
import { BookOpen, Cpu, ShieldAlert, GitCommit, CheckCircle2, ArrowRight } from 'lucide-react';

export default function Methodology() {
  const steps = [
    { title: 'User Input', desc: 'Select processor topology, simulation condition, shot count, and deterministic seed in the frontend form.' },
    { title: 'FastAPI Backend', desc: 'Validates parameters, enforces concurrency locks, and routes execution request to Python quantum engine.' },
    { title: 'Qiskit Aer Engine', desc: 'Constructs Bell circuits, applies basis rotations (H, S†), compiles to target CouplingMap, and runs depolarizing noise model.' },
    { title: 'Postselection Filter', desc: 'Inspects classical ancilla register c2; accepts shots with c2 = 0, discards corrupted shots with c2 = 1.' },
    { title: 'Statistical Analysis', desc: 'Computes signed expectation values ⟨XX⟩, ⟨YY⟩, ⟨ZZ⟩, fidelity F, and propagates Gaussian uncertainty σ_F.' },
    { title: 'Interactive Dashboard', desc: 'Renders verified metrics, sortable result tables, and high-resolution Recharts visualizations.' },
  ];

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Experimental Methodology & Physics Guide</h1>
        <p className="page-description">
          A beginner-friendly scientific explanation of quantum error detection, Bell state tomography,
          and NISQ decoherence trade-offs.
        </p>
      </div>

      {/* End-to-End Workflow Diagram */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <div className="card-header">
          <h3 className="card-title">
            <GitCommit size={18} style={{ color: 'var(--accent-cyan)' }} />
            <span>End-to-End System Workflow</span>
          </h3>
          <span className="brand-badge">Architecture</span>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem', marginTop: '1rem' }}>
          {steps.map((s, idx) => (
            <div
              key={idx}
              style={{
                background: 'var(--bg-tertiary)',
                borderRadius: '8px',
                padding: '1rem',
                border: '1px solid var(--border-color)',
                position: 'relative',
              }}
            >
              <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--accent-cyan)', textTransform: 'uppercase', marginBottom: '0.4rem' }}>
                Step 0{idx + 1}
              </div>
              <div style={{ fontWeight: 600, fontSize: '0.95rem', marginBottom: '0.35rem' }}>{s.title}</div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{s.desc}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Core Concepts Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
        <div className="card">
          <h3 className="card-title" style={{ marginBottom: '1rem' }}>1. What is a Qubit & a Bell State?</h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem', marginBottom: '0.75rem' }}>
            Unlike a classical bit that is either 0 or 1, a quantum bit (<strong>qubit</strong>) can exist in a linear superposition:
            <code style={{ display: 'block', padding: '0.5rem', background: 'var(--bg-tertiary)', borderRadius: '6px', margin: '0.5rem 0', fontFamily: 'var(--font-mono)' }}>
              |ψ⟩ = α|0⟩ + β|1⟩, where |α|² + |β|² = 1
            </code>
          </p>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem' }}>
            A <strong>Bell State</strong> is a maximally entangled two-qubit state where measuring one qubit instantaneously determines the outcome of the other. Q-Guard prepares the symmetric Bell state:
            <code style={{ display: 'block', padding: '0.5rem', background: 'var(--bg-tertiary)', borderRadius: '6px', margin: '0.5rem 0', fontFamily: 'var(--font-mono)' }}>
              |Φ⁺⟩ = (|00⟩ + |11⟩) / √2
            </code>
          </p>
        </div>

        <div className="card">
          <h3 className="card-title" style={{ marginBottom: '1rem' }}>2. Multi-Basis Pauli Measurements</h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem', marginBottom: '0.75rem' }}>
            Standard quantum hardware only measures directly in the computational Z-basis ({'|0⟩, |1⟩'}). To measure non-commuting Pauli observables, pre-measurement unitary rotations are applied:
          </p>
          <ul style={{ paddingLeft: '1.25rem', color: 'var(--text-secondary)', fontSize: '0.9rem', display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
            <li><strong>ZZ Observable:</strong> Direct computational measurement. Expected ideal: <code>+1.0</code></li>
            <li><strong>XX Observable:</strong> Apply Hadamard (H) before measurement. Expected ideal: <code>+1.0</code></li>
            <li><strong>YY Observable:</strong> Apply Phase dagger (S†) then Hadamard (H). Expected ideal: <code>-1.0</code></li>
          </ul>
        </div>

        <div className="card">
          <h3 className="card-title" style={{ marginBottom: '1rem' }}>3. Bell-State Fidelity & Uncertainty</h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem', marginBottom: '0.75rem' }}>
            For the target state |Φ⁺⟩, quantum fidelity F represents the overlap with the ideal entangled state:
            <code style={{ display: 'block', padding: '0.5rem', background: 'var(--bg-tertiary)', borderRadius: '6px', margin: '0.5rem 0', fontFamily: 'var(--font-mono)' }}>
              F(ρ, |Φ⁺⟩) = (1 + ⟨XX⟩ - ⟨YY⟩ + ⟨ZZ⟩) / 4
            </code>
          </p>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem' }}>
            Because each Pauli observable M is sampled independently with NM shots, Gaussian error propagation yields standard error:
            <code style={{ display: 'block', padding: '0.5rem', background: 'var(--bg-tertiary)', borderRadius: '6px', margin: '0.5rem 0', fontFamily: 'var(--font-mono)' }}>
              σ_F = (1/4) · √(σ_XX² + σ_YY² + σ_ZZ²)
            </code>
          </p>
        </div>

        <div className="card">
          <h3 className="card-title" style={{ marginBottom: '1rem' }}>4. Classical Entanglement Threshold</h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem', marginBottom: '0.75rem' }}>
            Any classical or unentangled separable state cannot achieve fidelity greater than <strong>0.50</strong> with |Φ⁺⟩.
          </p>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem' }}>
            To rigorously certify genuine quantum entanglement with 95.4% statistical confidence (2 standard deviations), Q-Guard evaluates:
            <code style={{ display: 'block', padding: '0.5rem', background: 'var(--bg-tertiary)', borderRadius: '6px', margin: '0.5rem 0', fontFamily: 'var(--font-mono)', color: 'var(--status-success)' }}>
              Threshold Rule: F - 2σ_F &gt; 0.50
            </code>
          </p>
        </div>
      </div>

      {/* Detection Scope and NISQ Trade-off */}
      <div className="card" style={{ borderLeft: '4px solid var(--status-warning)' }}>
        <h3 className="card-title" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <ShieldAlert size={20} style={{ color: 'var(--status-warning)' }} />
          <span>Error Detection Scope & The NISQ Noise Trade-off</span>
        </h3>
        <div style={{ marginTop: '0.75rem', color: 'var(--text-secondary)', fontSize: '0.92rem', lineHeight: '1.6' }}>
          <p style={{ marginBottom: '0.75rem' }}>
            <strong>What the Parity Check Can Detect:</strong> The ancilla measures the parity operator <code>Z ⊗ Z</code>.
            Single-qubit bit-flip errors (<strong>X</strong>) and bit-phase errors (<strong>Y</strong>) anti-commute with Z, flipping the ancilla qubit to <code>|1⟩</code>, which postselection successfully detects and discards.
          </p>
          <p style={{ marginBottom: '0.75rem' }}>
            <strong>What It Cannot Detect:</strong> Phase-flip errors (<strong>Z</strong>) commute with <code>Z ⊗ Z</code>. Therefore, phase-flip errors leave the ancilla in state <code>|0⟩</code>, allowing distorted states (|Φ⁻⟩) to pass postselection undetected.
          </p>
          <p>
            <strong>Why Protected Fidelity is Lower:</strong> Adding the ancilla parity check requires 2 additional CNOT gates and up to 3 routing CNOTs (+5 depth, +5 two-qubit CX gates). In current NISQ hardware with physical 2-qubit gate error rates of 1%–2.5%, the physical noise introduced by the extraction circuit exceeds the error-filtering capacity of postselection.
          </p>
        </div>
      </div>
    </div>
  );
}
