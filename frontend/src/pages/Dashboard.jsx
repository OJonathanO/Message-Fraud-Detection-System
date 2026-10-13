import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Shield, AlertTriangle, CheckCircle, Activity } from 'lucide-react'
import StatCard from '../components/StatCard'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorMessage from '../components/ErrorMessage'
import { CategoryBarChart, TrendLineChart, RiskLevelChart } from '../components/AnalyticsChart'
import { getAnalyticsSummary, getAnalyticsCategories, getAnalyticsTrends, getPredictions } from '../api/predictions'
import { formatDate, truncateText } from '../utils/formatters'
import RiskBadge from '../components/RiskBadge'

export default function Dashboard() {
  const [summary, setSummary] = useState(null)
  const [categories, setCategories] = useState(null)
  const [trends, setTrends] = useState(null)
  const [recentPredictions, setRecentPredictions] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    setLoading(true)
    setError(null)
    try {
      const [summaryRes, categoriesRes, trendsRes, predictionsRes] = await Promise.all([
        getAnalyticsSummary(),
        getAnalyticsCategories(),
        getAnalyticsTrends(),
        getPredictions({ per_page: 5 }),
      ])
      setSummary(summaryRes)
      setCategories(categoriesRes)
      setTrends(trendsRes)
      setRecentPredictions(predictionsRes.predictions || [])
    } catch (err) {
      setError(err.message || 'Failed to load dashboard data')
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <LoadingSpinner message="Loading dashboard..." />
  if (error) return <ErrorMessage message={error} onRetry={loadDashboardData} />

  return (
    <div className="page dashboard-page">
      <div className="page-header">
        <h1>Dashboard</h1>
        <p>Overview of message analysis activity</p>
      </div>

      <div className="stats-grid">
        <StatCard
          title="Total Analyzed"
          value={summary?.total_messages || 0}
          icon={<Shield size={24} />}
          color="#3b82f6"
        />
        <StatCard
          title="Suspicious"
          value={summary?.suspicious_count || 0}
          icon={<AlertTriangle size={24} />}
          color="#ef4444"
        />
        <StatCard
          title="Legitimate"
          value={summary?.legitimate_count || 0}
          icon={<CheckCircle size={24} />}
          color="#10b981"
        />
        <StatCard
          title="Risk Distribution"
          value={Object.keys(summary?.risk_distribution || {}).length}
          icon={<Activity size={24} />}
          color="#f59e0b"
        />
      </div>

      <div className="dashboard-charts">
        <div className="chart-card">
          <h3>Category Distribution</h3>
          <CategoryBarChart data={categories?.categories} />
        </div>
        <div className="chart-card">
          <h3>Risk Level Distribution</h3>
          <RiskLevelChart data={summary?.risk_distribution} />
        </div>
        <div className="chart-card chart-wide">
          <h3>Prediction Trends</h3>
          <TrendLineChart data={trends?.trends} />
        </div>
      </div>

      <div className="recent-predictions">
        <div className="section-header">
          <h3>Recent Predictions</h3>
          <Link to="/history" className="btn btn-secondary">View All</Link>
        </div>
        {recentPredictions.length === 0 ? (
          <div className="empty-state">
            <p>No predictions yet. <Link to="/analyzer">Analyze your first message</Link>.</p>
          </div>
        ) : (
          <div className="prediction-list">
            {recentPredictions.map((pred) => (
              <div key={pred.id} className="prediction-list-item">
                <div className="prediction-list-message">
                  {truncateText(pred.message, 80)}
                </div>
                <div className="prediction-list-meta">
                  <RiskBadge riskLevel={pred.risk_level} />
                  <span className="prediction-date">{formatDate(pred.created_at)}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="quick-action">
        <Link to="/analyzer" className="btn btn-primary btn-large">
          Analyze New Message
        </Link>
      </div>
    </div>
  )
}
