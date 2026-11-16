import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from "recharts";
import '../styles/chart.css'

function ForecastChart({ data }) {
  return (
    <div className="chart-container">
      <h2>Actual vs Forecast Wind Generation</h2>

      <ResponsiveContainer width="100%" height={350}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis
            dataKey="delivery_time"
            tickFormatter={(value) => value.slice(5, 16)}
          />

          <YAxis />

          <Tooltip />

          <Legend />

          <Line
            type="monotone"
            dataKey="actual_generation"
            name="Actual Generation"
            stroke="#2563eb"
            dot={false}
          />

          <Line
            type="monotone"
            dataKey="forecast_generation"
            name="Forecast Generation"
            stroke="#f97316"
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default ForecastChart;