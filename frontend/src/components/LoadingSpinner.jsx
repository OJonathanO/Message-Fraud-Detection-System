export default function LoadingSpinner({ size = 'medium', message = 'Loading...' }) {
  const sizeMap = {
    small: '20px',
    medium: '40px',
    large: '60px',
  }

  return (
    <div className="loading-spinner-container">
      <div
        className="loading-spinner"
        style={{
          width: sizeMap[size],
          height: sizeMap[size],
        }}
      />
      {message && <p className="loading-message">{message}</p>}
    </div>
  )
}
