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

export default function FidelityChart({ data }) {
  if (!data || data.length === 0) {
    return <div className="empty-state">No fidelity data available.</div>;
  }

  // Transform data for grouped bar chart
  const processorMap = {};
  data.forEach((item) => {
    const proc = item.processor;
    if (!processorMap[proc]) {
      processorMap[proc] = { processor: proc };
    }
    if (item.experiment === 'Ideal') {
      processorMap[proc].Ideal = item.fidelity_estimate;
    } else if (item.experiment === 'Noisy') {
      processorMap[proc].Noisy = item.fidelity_estimate;
    } else if (item.experiment === 'Noisy + Protection') {
      processorMap[proc]['Protected'] = item.fidelity_estimate;
    }
  });

  const chartData = Object.values(processorMap);

  return (
    <div style={{ width: '100%', height: 320 }}>
      <ResponsiveContainer>
        <BarChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#232f4c" />
          <XAxis dataKey="processor" stroke="#94a3b8" tick={{ fill: '#94a3b8' }} />
          <YAxis domain={[0, 1.05]} stroke="#94a3b8" tick={{ fill: '#94a3b8' }} />
          <Tooltip
            contentStyle={{
              backgroundColor: '#111726',
              borderColor: '#232f4c',
              borderRadius: '8px',
              color: '#f1f5f9',
            }}
            formatter={(value) => [`${(value * 100).toFixed(2)}% (F = ${value})`, 'Fidelity']}
          />
          <Legend wrapperStyle={{ paddingTop: '10px' }} />
          <ReferenceLine
            y={0.5}
            stroke="#ef4444"
            strokeDasharray="4 4"
            label={{ value: 'Classical Bound (0.50)', fill: '#ef4444', position: 'top', fontSize: 12 }}
          />
          <Bar dataKey="Ideal" fill="#38bdf8" radius={[4, 4, 0, 0]} name="Ideal State" />
          <Bar dataKey="Noisy" fill="#f59e0b" radius={[4, 4, 0, 0]} name="Noisy Baseline" />
          <Bar dataKey="Protected" fill="#8b5cf6" radius={[4, 4, 0, 0]} name="Protected (Postselection)" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
