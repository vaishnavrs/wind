import React from 'react';  
import '../styles/kpi.css';

function KpiCard({ title, value, unit, description }) {
  return (
    <div className="kpi-card">
      <p className="kpi-title">{title}</p>

      <h2 className="kpi-value">{value}</h2>

      <p className="kpi-unit">{unit}</p>

      <p className="kpi-description">{description}</p>
    </div>
  );SsSSS
}

export default KpiCard;