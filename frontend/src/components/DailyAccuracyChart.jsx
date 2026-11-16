import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from "recharts";

function DailyAccuracyChart({ data }) {
  return (
    <div className="chart-container">
      <h2>Daily Forecast Accuracy</h2>

      <ResponsiveContainer width="100%" height={350}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="date" />

          <YAxis />

          <Tooltip />

          <Legend />

          <Bar
            dataKey="mae"
            name="Daily MAE"
            fill="#2563eb"
          />

          <Bar
            dataKey="bias"
            name="Daily Bias"
            fill="#f97316"
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default DailyAccuracyChart;