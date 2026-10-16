import React from 'react';

export default function LoadingState({ message = 'Running quantum circuit simulation...' }) {
  return (
    <div className="loading-box">
      <div className="spinner"></div>
      <p style={{ fontWeight: 500, color: 'var(--text-primary)' }}>{message}</p>
      <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: '0.35rem' }}>
        Transpiling basis gates, evaluating depolarizing noise, and measuring Pauli correlations
      </p>
    </div>
  );
}
