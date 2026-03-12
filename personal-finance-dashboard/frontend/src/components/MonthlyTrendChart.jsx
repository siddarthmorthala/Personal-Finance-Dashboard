import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

export default function MonthlyTrendChart({ data }) {
  return (
    <section className="card chart-card">
      <h2>Monthly Trends</h2>
      <p className="card-description">Compare monthly income and spending over time.</p>
      <div className="chart-wrapper">
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="income" />
            <Line type="monotone" dataKey="spending" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </section>
  )
}
