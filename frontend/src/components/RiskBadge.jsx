import { getRiskConfig } from '../utils/riskConfig'

export default function RiskBadge({ riskLevel }) {
  const config = getRiskConfig(riskLevel)

  return (
    <span
      className="risk-badge"
      style={{
        color: config.color,
        backgroundColor: config.bgColor,
        borderColor: config.borderColor,
      }}
    >
      {config.label} Risk
    </span>
  )
}
