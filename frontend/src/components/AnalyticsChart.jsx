import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  Legend,
} from 'recharts'

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']

export function CategoryBarChart({ data }) {
  if (!data || Object.keys(data).length === 0) {
    return <div className="chart-empty">No data available</div>
  }

  const chartData = Object.entries(data).map(([name, value]) => ({
    name: name === 'spam' ? 'Spam' : name === 'ham' ? 'Legitimate' : name,
    value,
  }))

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
        <XAxis dataKey="name" stroke="#9ca3af" />
        <YAxis stroke="#9ca3af" />
        <Tooltip
          contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }}
        />
        <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  )
}

export function CategoryPieChart({ data }) {
  if (!data || Object.keys(data).length === 0) {
    return <div className="chart-empty">No data available</div>
  }

  const chartData = Object.entries(data).map(([name, value]) => ({
    name: name === 'spam' ? 'Spam' : name === 'ham' ? 'Legitimate' : name,
    value,
  }))

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={chartData}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
          outerRadius={100}
          fill="#8884d8"
          dataKey="value"
        >
          {chartData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }}
        />
      </PieChart>
    </ResponsiveContainer>
  )
}

export function TrendLineChart({ data }) {
  if (!data || data.length === 0) {
    return <div className="chart-empty">No trend data available</div>
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
        <XAxis dataKey="date" stroke="#9ca3af" />
        <YAxis stroke="#9ca3af" />
        <Tooltip
          contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }}
        />
        <Legend />
        <Line type="monotone" dataKey="spam" stroke="#ef4444" strokeWidth={2} name="Spam" />
        <Line type="monotone" dataKey="ham" stroke="#10b981" strokeWidth={2} name="Legitimate" />
      </LineChart>
    </ResponsiveContainer>
  )
}

export function RiskLevelChart({ data }) {
  if (!data || Object.keys(data).length === 0) {
    return <div className="chart-empty">No data available</div>
  }

  const chartData = Object.entries(data).map(([level, count]) => ({
    level: level.charAt(0).toUpperCase() + level.slice(1),
    count,
    fill: level === 'low' ? '#10b981' : level === 'medium' ? '#f59e0b' : level === 'high' ? '#ef4444' : '#dc2626',
  }))

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
        <XAxis dataKey="level" stroke="#9ca3af" />
        <YAxis stroke="#9ca3af" />
        <Tooltip
          contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }}
        />
        <Bar dataKey="count" radius={[4, 4, 0, 0]}>
          {chartData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.fill} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}
