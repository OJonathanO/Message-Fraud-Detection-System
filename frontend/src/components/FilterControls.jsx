import { Search, Filter } from 'lucide-react'

export default function FilterControls({ filters, onFilterChange, onClear }) {
  const handleChange = (key, value) => {
    onFilterChange({ ...filters, [key]: value })
  }

  return (
    <div className="filter-controls">
      <div className="filter-group">
        <div className="filter-search">
          <Search size={16} />
          <input
            type="text"
            placeholder="Search messages..."
            value={filters.search || ''}
            onChange={(e) => handleChange('search', e.target.value)}
            className="filter-input"
          />
        </div>
      </div>

      <div className="filter-group">
        <Filter size={16} />
        <select
          value={filters.category || ''}
          onChange={(e) => handleChange('category', e.target.value)}
          className="filter-select"
        >
          <option value="">All Categories</option>
          <option value="spam">Spam</option>
          <option value="ham">Legitimate</option>
        </select>
      </div>

      <div className="filter-group">
        <select
          value={filters.riskLevel || ''}
          onChange={(e) => handleChange('riskLevel', e.target.value)}
          className="filter-select"
        >
          <option value="">All Risk Levels</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
          <option value="critical">Critical</option>
        </select>
      </div>

      <div className="filter-group">
        <input
          type="date"
          value={filters.dateFrom || ''}
          onChange={(e) => handleChange('dateFrom', e.target.value)}
          className="filter-input"
          placeholder="From date"
        />
      </div>

      <div className="filter-group">
        <input
          type="date"
          value={filters.dateTo || ''}
          onChange={(e) => handleChange('dateTo', e.target.value)}
          className="filter-input"
          placeholder="To date"
        />
      </div>

      <button className="btn btn-secondary" onClick={onClear}>
        Clear Filters
      </button>
    </div>
  )
}
