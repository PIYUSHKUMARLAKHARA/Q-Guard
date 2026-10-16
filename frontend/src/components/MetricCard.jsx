import React from 'react';

export default function MetricCard({ label, value, subtext, icon: Icon, color = 'cyan', tooltip }) {
  return (
    <div className="metric-card" title={tooltip || ''}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <span className="metric-label">{label}</span>
        {Icon && <Icon size={18} style={{ color: `var(--accent-${color})`, opacity: 0.8 }} />}
      </div>
      <div className="metric-value">{value}</div>
      {subtext && <div className="metric-sub">{subtext}</div>}
    </div>
  );
}
