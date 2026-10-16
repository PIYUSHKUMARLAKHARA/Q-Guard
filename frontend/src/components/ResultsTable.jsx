import React, { useState } from 'react';
import { ArrowUpDown, CheckCircle2, XCircle } from 'lucide-react';

export default function ResultsTable({ data, onSelectRow, selectedId }) {
  const [sortField, setSortField] = useState('fidelity_estimate');
  const [sortOrder, setSortOrder] = useState('desc');

  if (!data || data.length === 0) {
    return <div className="empty-state">No experiment results recorded yet.</div>;
  }

  const handleSort = (field) => {
    if (sortField === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortOrder('desc');
    }
  };

  const sortedData = [...data].sort((a, b) => {
    let aVal = a[sortField];
    let bVal = b[sortField];
    if (typeof aVal === 'string') {
      return sortOrder === 'asc' ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
    }
    return sortOrder === 'asc' ? aVal - bVal : bVal - aVal;
  });

  return (
    <div className="table-container">
      <table className="data-table">
        <thead>
          <tr>
            <th onClick={() => handleSort('processor')} style={{ cursor: 'pointer' }}>
              Processor <ArrowUpDown size={12} />
            </th>
            <th onClick={() => handleSort('experiment')} style={{ cursor: 'pointer' }}>
              Experiment <ArrowUpDown size={12} />
            </th>
            <th onClick={() => handleSort('fidelity_estimate')} style={{ cursor: 'pointer' }}>
              Fidelity (F) <ArrowUpDown size={12} />
            </th>
            <th>Uncertainty (±2σ)</th>
            <th>Threshold (&gt; 0.5)</th>
            <th onClick={() => handleSort('acceptance_rate')} style={{ cursor: 'pointer' }}>
              Acceptance <ArrowUpDown size={12} />
            </th>
            <th>Accepted Shots</th>
            <th>Depth</th>
            <th>2Q Gates</th>
          </tr>
        </thead>
        <tbody>
          {sortedData.map((row, index) => {
            const isSelected = selectedId === row.id;
            return (
              <tr
                key={row.id || index}
                onClick={() => onSelectRow && onSelectRow(row)}
                style={{
                  cursor: onSelectRow ? 'pointer' : 'default',
                  backgroundColor: isSelected ? 'rgba(0, 242, 254, 0.08)' : undefined,
                  borderLeft: isSelected ? '3px solid var(--accent-cyan)' : undefined,
                }}
              >
                <td style={{ fontWeight: 600 }}>{row.processor}</td>
                <td>
                  <span
                    className="badge"
                    style={{
                      background:
                        row.experiment === 'Ideal'
                          ? 'rgba(56, 189, 248, 0.15)'
                          : row.experiment === 'Noisy'
                          ? 'rgba(245, 158, 11, 0.15)'
                          : 'rgba(139, 92, 246, 0.15)',
                      color:
                        row.experiment === 'Ideal'
                          ? '#38bdf8'
                          : row.experiment === 'Noisy'
                          ? '#f59e0b'
                          : '#c084fc',
                    }}
                  >
                    {row.experiment}
                  </span>
                </td>
                <td style={{ fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
                  {row.fidelity_estimate.toFixed(5)}
                </td>
                <td style={{ fontFamily: 'var(--font-mono)', color: 'var(--text-secondary)' }}>
                  ±{(row.fidelity_uncertainty * 2).toFixed(5)}
                </td>
                <td>
                  {row.threshold_passed ? (
                    <span className="badge badge-pass">
                      <CheckCircle2 size={12} style={{ marginRight: 4 }} />
                      PASS
                    </span>
                  ) : (
                    <span className="badge badge-fail">
                      <XCircle size={12} style={{ marginRight: 4 }} />
                      FAIL
                    </span>
                  )}
                </td>
                <td style={{ fontFamily: 'var(--font-mono)' }}>
                  {(row.acceptance_rate * 100).toFixed(1)}%
                </td>
                <td style={{ fontFamily: 'var(--font-mono)' }}>
                  {row.accepted_shots_avg} / {row.total_shots_avg || row.shots_per_observable}
                </td>
                <td style={{ fontFamily: 'var(--font-mono)' }}>
                  {row.average_circuit_depth?.toFixed(1) || 'N/A'}
                </td>
                <td style={{ fontFamily: 'var(--font-mono)' }}>
                  {row.average_two_qubit_gates?.toFixed(1) || 'N/A'}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
