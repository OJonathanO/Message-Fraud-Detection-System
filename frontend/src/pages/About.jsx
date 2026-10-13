export default function About() {
  return (
    <div className="page about-page">
      <div className="page-header">
        <h1>About This Project</h1>
        <p>Learn about the technology and methodology behind the system</p>
      </div>

      <div className="about-content">
        <section className="about-section">
          <h2>Problem Statement</h2>
          <p>
            SMS spam and phishing messages are a persistent threat to mobile users worldwide.
            These unwanted messages can lead to financial loss, identity theft, and privacy
            violations. Traditional rule-based filters struggle to keep up with evolving
            spam techniques.
          </p>
          <p>
            This system applies machine learning to automatically classify text messages,
            providing users with an additional layer of protection against unwanted
            communications.
          </p>
        </section>

        <section className="about-section">
          <h2>Technology Stack</h2>
          <div className="tech-grid">
            <div className="tech-item">
              <h4>Frontend</h4>
              <ul>
                <li>React with Vite</li>
                <li>React Router</li>
                <li>Axios</li>
                <li>Recharts</li>
                <li>Lucide Icons</li>
              </ul>
            </div>
            <div className="tech-item">
              <h4>Backend</h4>
              <ul>
                <li>Python Flask</li>
                <li>SQLAlchemy ORM</li>
                <li>Flask-CORS</li>
                <li>Flask-Limiter</li>
                <li>Gunicorn</li>
              </ul>
            </div>
            <div className="tech-item">
              <h4>Machine Learning</h4>
              <ul>
                <li>Scikit-learn</li>
                <li>TF-IDF Vectorizer</li>
                <li>Logistic Regression</li>
                <li>Pandas</li>
                <li>Joblib</li>
              </ul>
            </div>
            <div className="tech-item">
              <h4>Database</h4>
              <ul>
                <li>SQLite (development)</li>
                <li>PostgreSQL-ready</li>
              </ul>
            </div>
          </div>
        </section>

        <section className="about-section">
          <h2>NLP and ML Workflow</h2>
          <ol className="workflow-list">
            <li><strong>Text Preprocessing:</strong> Lowercasing, URL/email/phone/currency normalization, repeated character collapsing</li>
            <li><strong>Feature Extraction:</strong> TF-IDF vectorization with unigrams and bigrams (max 10,000 features)</li>
            <li><strong>Classification:</strong> Logistic Regression with balanced class weights</li>
            <li><strong>Evaluation:</strong> Stratified train-test split (80/20) with accuracy, precision, recall, and F1 metrics</li>
            <li><strong>Explainability:</strong> Feature importance extraction from Logistic Regression coefficients</li>
          </ol>
        </section>

        <section className="about-section">
          <h2>System Architecture</h2>
          <p>
            The system follows a client-server architecture with a React frontend
            communicating with a Flask REST API backend. The ML model is loaded once
            at startup and reused for all predictions. Prediction history is persisted
            in SQLite with support for PostgreSQL migration.
          </p>
        </section>

        <section className="about-section">
          <h2>Ethical Considerations</h2>
          <ul>
            <li>The model is trained on publicly available data and does not collect personal information</li>
            <li>Prediction history is stored locally and can be deleted by the user</li>
            <li>The system does not claim to detect all fraud or phishing attempts</li>
            <li>Users are encouraged to verify suspicious messages through official channels</li>
            <li>Message content is processed by the application and may be stored if history is enabled</li>
          </ul>
        </section>

        <section className="about-section">
          <h2>Limitations</h2>
          <ul>
            <li><strong>Binary classification only:</strong> The model classifies messages as spam or legitimate. It does not detect fraud or phishing specifically.</li>
            <li><strong>Limited to SMS:</strong> Trained on SMS messages; may not generalize to emails or other formats.</li>
            <li><strong>English only:</strong> The model is trained on English-language messages.</li>
            <li><strong>Not real-time:</strong> Does not integrate with email or SMS providers.</li>
            <li><strong>Educational purpose:</strong> Designed for learning, not as a production security tool.</li>
          </ul>
        </section>

        <section className="about-section">
          <h2>Future Enhancements</h2>
          <ul>
            <li>Multi-class classification with fraud and phishing detection</li>
            <li>Email and URL analysis capabilities</li>
            <li>Real-time API integration with email/SMS providers</li>
            <li>User authentication and personalized models</li>
            <li>Advanced explainability with SHAP values</li>
            <li>Mobile application</li>
          </ul>
        </section>
      </div>
    </div>
  )
}
