import { useState, useEffect } from "react";
import Navbar from "./components/Navbar";
import ForecastChart from "./components/ForeCastChart";
import Sidebar from "./components/SideBar";
import KpiCard from "./components/KpiCard";
import DailyAccuracyChart from "./components/DailyAccuracyChart";
import API from "./services/api";
import "./App.css";

function App() {
  const [dashboardData, setDashboardData] = useState(null);
  const [forecastData, setForecastData] = useState([]);
  const [selectedDate, setSelectedDate] = useState("2026-01-15");
  const [dailyAccuracy, setDailyAccuracy] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Filter forecast records based on the selected delivery date
  const filteredForecastData = forecastData.filter((record) => {
    return record.delivery_time.startsWith(selectedDate);
  });

  // Fetch dashboard data from Django backend
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError("");

        const dashboardResponse = await API.get("dashboard/");
        const forecastResponse = await API.get("forecasts/");
        const dailyResponse = await API.get("daily-accuracy/");

        setDashboardData(dashboardResponse.data);
        setForecastData(forecastResponse.data);
        setDailyAccuracy(dailyResponse.data);

      } catch (error) {
        console.error("Error fetching dashboard:", error);
        setError("Unable to load dashboard data. Please try again.");

      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="app-layout">

      <Sidebar />

      <div className="main-content">

        <Navbar />

        {loading ? (
          <div className="status-message">
            Loading dashboard data...
          </div>

        ) : error ? (
          <div className="status-message error-message">
            <p>{error}</p>

            <button onClick={() => window.location.reload()}>
              Retry
            </button>
          </div>

        ) : !dashboardData ? (
          <div className="status-message">
            No dashboard data available.
          </div>

        ) : (
          <main className="dashboard">

            {/* OVERVIEW SECTION */}
            <section id="overview">

              <h2>Wind Generation Overview</h2>

              <div className="kpi-grid">

                <KpiCard
                  title="Mean Absolute Error"
                  value={dashboardData.mae}
                  unit="MW"
                  description="Average absolute forecast error"
                />

                <KpiCard
                  title="Root Mean Square Error"
                  value={dashboardData.rmse}
                  unit="MW"
                  description="Penalises larger errors"
                />

                <KpiCard
                  title="Forecast Bias"
                  value={dashboardData.bias}
                  unit="MW"
                  description="Forecasts tend to overestimate"
                />

                <KpiCard
                  title="Data Coverage"
                  value={`${dashboardData.coverage_percentage}%`}
                  unit={`${dashboardData.matched_periods} / ${dashboardData.expected_periods} periods`}
                  description="Matched hourly periods"
                />

              </div>
            </section>

            {/* FORECAST ANALYSIS SECTION */}
            <section id="forecast-analysis">

              <h2>Forecast Analysis</h2>

              <div className="date-filter">

                <label htmlFor="delivery-date">
                  Select delivery date:
                </label>

                <input
                  id="delivery-date"
                  type="date"
                  min="2026-01-01"
                  max="2026-01-31"
                  value={selectedDate}
                  onChange={(event) =>
                    setSelectedDate(event.target.value)
                  }
                />

              </div>

              <ForecastChart data={filteredForecastData} />

            </section>

            {/* DAILY ACCURACY SECTION */}
            <section id="daily-accuracy">

              <h2>Daily Forecast Accuracy</h2>

              <DailyAccuracyChart data={dailyAccuracy} />

            </section>

            {/* DATA QUALITY SECTION */}
            
            <section id="data-quality">

              <h2>Data Quality & Coverage</h2>

              <div className="quality-grid">

                <div className="quality-card">
                  <h3>Expected Periods</h3>
                  <p>{dashboardData.expected_periods}</p>
                  <span>Hourly periods in January</span>
                </div>

                <div className="quality-card">
                  <h3>Matched Periods</h3>
                  <p>{dashboardData.matched_periods}</p>
                  <span>Periods with actual and forecast data</span>
                </div>

                <div className="quality-card">
                  <h3>Missing Periods</h3>
                  <p>{dashboardData.missing_periods}</p>
                  <span>Periods without an eligible forecast</span>
                </div>

                <div className="quality-card">
                  <h3>Coverage</h3>
                  <p>{dashboardData.coverage_percentage}%</p>
                  <span>Percentage of expected periods matched</span>
                </div>

              </div>

              <div className="quality-note">
                <h3>Data Availability</h3>
                <p>
                  The analysis matched {dashboardData.matched_periods} out of
                  {" "}{dashboardData.expected_periods} expected hourly periods.
                  The remaining {dashboardData.missing_periods} periods were
                  excluded because an eligible forecast was not available
                  before the selected decision cutoff.
                </p>
              </div>

            </section>

            {/* METHODOLOGY SECTION */}
            <section id="methodology">

              <h2>How We Calculate Forecast Accuracy</h2>

              <div className="methodology-grid">

                <div className="methodology-card">
                  <span className="method-number">01</span>
                  <h3>Forecast Selection</h3>
                  <p>
                    For each hourly delivery period, we select the latest
                    available wind forecast published on or before the
                    previous day's 10:00 UTC decision cutoff.
                  </p>
                </div>

                <div className="methodology-card">
                  <span className="method-number">02</span>
                  <h3>Actual Generation</h3>
                  <p>
                    Actual generation is recorded at 30-minute intervals.
                    We average the two half-hour readings to obtain one
                    hourly actual generation value.
                  </p>
                </div>

                <div className="methodology-card">
                  <span className="method-number">03</span>
                  <h3>Error Calculation</h3>
                  <p>
                    Forecast error is calculated by subtracting actual
                    generation from forecast generation.
                  </p>
                  <code>Forecast − Actual</code>
                </div>

              </div>

              <div className="methodology-note">
                <h3>Important Assumptions</h3>
                <ul>
                  <li>
                    The previous-day 10:00 UTC cutoff is an analytical
                    assumption used for this evaluation, not a confirmed
                    official market deadline.
                  </li>
                  <li>
                    Averaging two half-hour actual readings into one
                    hourly value is an analytical aggregation assumption.
                  </li>
                  <li>
                    The analysis focuses on wind generation forecasts.
                    It does not calculate total electricity procurement
                    requirements.
                  </li>
                </ul>
              </div>

            </section>



          </main>
        )}

      </div>
    </div>
  );
}

export default App;
