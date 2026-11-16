import React from "react";
import '../styles/sidebar.css'
function Sidebar() {
  return (
    <aside className="sidebar">

      <div className="sidebar-heading">
        <h3>WIND INSIGHTS</h3>
      </div>

      <nav className="sidebar-menu">

        <a href="#overview" className="active">
          <span>◈</span>
          Overview
        </a>

        <a href="#forecast-analysis">
          <span>↗</span>
          Forecast Analysis
        </a>

        <a href="#daily-accuracy">
          <span>▥</span>
          Daily Accuracy
        </a>

        <a href="#data-quality">
          <span>◉</span>
          Data Quality
        </a>

        <a href="#methodology">
          <span>ⓘ</span>
          Methodology
        </a>

      </nav>

      <div className="sidebar-footer">
        <p>WindSight UK</p>
        <small>Version 1.0</small>
      </div>

    </aside>
  );
}

export default Sidebar;