import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts';

export default function CorrelationChart({ experiment }) {
  if (!experiment) {
    return <div className="empty-state">Select an experiment to view correlation breakdown.</div>;
  }

  const data = [
    { observable: 'XX', measured: experiment.XX, ideal: 1.0, uncertainty: experiment.sigma_XX },
    { observable: 'YY', measured: experiment.YY, ideal: -1.0, uncertainty: experiment.sigma_YY },
    { observable: 'ZZ', measured: experiment.ZZ, ideal: 1.0, uncertainty: experiment.sigma_ZZ },
  ];

  return (
    <div style={{ width: '100%', height: 280 }}>
      <ResponsiveContainer>
        <BarChart data={data} margin={{ top: 15, right: 30, left: 0, bottom: 15 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#232f4c" />
          <XAxis dataKey="observable" stroke="#94a3b8" />
          <YAxis domain={[-1.1, 1.1]} stroke="#94a3b8" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#111726',
              borderColor: '#232f4c',
              borderRadius: '8px',
              color: '#f1f5f9',
            }}
            formatter={(value, name) => [value.toFixed(5), name === 'measured' ? 'Measured ⟨M⟩' : 'Ideal Target']}
          />
          <Legend />
          <ReferenceLine y={0} stroke="#475569" />
          <Bar dataKey="ideal" fill="#64748b" radius={[4, 4, 0, 0]} name="Ideal Value" />
          <Bar dataKey="measured" fill="#00f2fe" radius={[4, 4, 0, 0]} name="Measured Correlation" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
