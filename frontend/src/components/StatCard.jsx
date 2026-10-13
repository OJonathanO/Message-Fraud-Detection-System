export default function StatCard({ title, value, subtitle, icon, color = '#3b82f6' }) {
  return (
    <div className="stat-card" style={{ borderLeftColor: color }}>
      <div className="stat-card-content">
        <div className="stat-card-text">
          <p className="stat-card-title">{title}</p>
          <p className="stat-card-value">{value}</p>
          {subtitle && <p className="stat-card-subtitle">{subtitle}</p>}
        </div>
        {icon && (
          <div className="stat-card-icon" style={{ color }}>
            {icon}
          </div>
        )}
      </div>
    </div>
  )
}
