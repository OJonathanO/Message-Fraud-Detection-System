# Message Fraud Detection System

A full-stack web application that uses machine learning to classify text messages as spam or legitimate. Built with Flask, React, and scikit-learn.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![React](https://img.shields.io/badge/React-18-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Project Overview

The Message Fraud Detection System analyzes text messages, emails, and notifications to identify potential spam using Natural Language Processing (NLP) and Machine Learning. The system uses a TF-IDF + Logistic Regression pipeline trained on the UCI SMS Spam Collection dataset.

**Important:** This is a **binary classifier** (spam vs. legitimate). It does NOT detect fraud or phishing specifically. Those categories require separate labeled datasets.

## Key Features

- **Message Classification**: Analyze text messages for spam indicators using ML
- **Risk Assessment**: Four-tier risk levels (Low, Medium, High, Critical)
- **Model Explainability**: See which terms influenced the prediction
- **Prediction History**: Searchable, filterable, sortable history with CSV export
- **Analytics Dashboard**: Visualize trends, category distribution, and risk levels
- **REST API**: Full Flask API with validation, rate limiting, and error handling
- **Docker Support**: Containerized deployment with Docker Compose

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite, React Router, Recharts, Lucide Icons |
| Backend | Python 3.11, Flask 3.0, SQLAlchemy, Flask-CORS, Flask-Limiter |
| ML/NLP | Scikit-learn, TF-IDF Vectorizer, Logistic Regression |
| Database | SQLite (development), PostgreSQL-ready |
| Testing | Pytest, Vitest, React Testing Library |
| Deployment | Docker, Docker Compose |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend                          │
│  (Dashboard, Analyzer, History, Model Performance, About)   │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/JSON (Axios)
┌──────────────────────────▼──────────────────────────────────┐
│                    Flask REST API                           │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │   Health    │  │  Prediction  │  │    Analytics      │  │
│  │  Blueprint  │  │  Blueprint   │  │    Blueprint      │  │
│  └─────────────┘  └──────┬───────┘  └───────────────────┘  │
│                          │                                  │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │              Prediction Service                       │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐  │  │
│  │  │   Model     │  │ Explainability│  │   Risk      │  │  │
│  │  │  Predictor  │  │   Engine      │  │ Assessment  │  │  │
│  │  └─────────────┘  └──────────────┘  └─────────────┘  │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                  │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │         TF-IDF + Logistic Regression Pipeline        │  │
│  │    (Loaded once at startup, reused for all requests) │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                  │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │              SQLite Database (SQLAlchemy)             │  │
│  │         ┌─────────────────────────────────┐          │  │
│  │         │      predictions table          │          │  │
│  │         │  (id, message, class, risk,     │          │  │
│  │         │   confidence, version, timestamp)│          │  │
│  │         └─────────────────────────────────┘          │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Machine Learning Workflow

```
┌──────────────┐    ┌──────────────┐    ┌──────────────────┐
│    UCI SMS   │    │   Download   │    │  Load & Validate │
│   Dataset    │───▶│   Dataset    │───▶│     Dataset      │
└──────────────┘    └──────────────┘    └────────┬─────────┘
                                                │
                       ┌────────────────────────▼─────┐
                       │   Remove Duplicates & Missing  │
                       │         Values                 │
                       └────────────────────────┬─────┘
                                                │
                       ┌────────────────────────▼─────┐
                       │   Stratified Train/Test Split  │
                       │         (80/20)               │
                       └────────────────────────┬─────┘
                                                │
         ┌──────────────────────────────────────┼──────────────────────┐
         │                                      │                      │
         ▼                                      ▼                      ▼
┌─────────────────┐                  ┌─────────────────┐      ┌─────────────────┐
│  Text           │                  │    TF-IDF       │      │  Logistic       │
│  Preprocessing  │─────────────────▶│  Vectorization  │─────▶│  Regression     │
│  (normalize,    │                  │  (1-2 grams,    │      │  (balanced      │
│   tokenize)     │                  │   10K features) │      │   classes)      │
└─────────────────┘                  └─────────────────┘      └────────┬────────┘
                                                                      │
                       ┌──────────────────────────────────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   Evaluate on   │
              │   Test Set      │
              │ (accuracy, F1,  │
              │  precision,     │
              │  recall)        │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Save Model     │
              │  Artifact       │
              │  (versioned)    │
              └─────────────────┘
```

## Project Structure

```
message-fraud-detection/
├── frontend/                 # React frontend
│   ├── public/
│   ├── src/
│   │   ├── api/             # API client and endpoints
│   │   ├── assets/          # Static assets
│   │   ├── components/      # Reusable UI components
│   │   ├── hooks/           # Custom React hooks
│   │   ├── layouts/         # Page layouts
│   │   ├── pages/           # Page components
│   │   ├── utils/           # Utility functions
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── backend/                  # Flask backend
│   ├── app/
│   │   ├── __init__.py      # Application factory
│   │   ├── config.py        # Configuration
│   │   ├── extensions.py    # Flask extensions
│   │   ├── models/          # Database models
│   │   ├── routes/          # API blueprints
│   │   ├── schemas/         # Request/response schemas
│   │   ├── services/        # Business logic
│   │   ├── ml/              # ML pipeline
│   │   │   ├── preprocessing.py
│   │   │   ├── train.py
│   │   │   ├── predictor.py
│   │   │   └── explainability.py
│   │   └── utils/           # Utilities
│   ├── tests/               # Backend tests
│   ├── scripts/             # Utility scripts
│   ├── requirements.txt
│   └── run.py
├── datasets/                # Dataset storage
├── model_artifacts/         # Trained model storage
├── docs/                    # Documentation
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+ and npm
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/message-fraud-detection.git
   cd message-fraud-detection
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Train the model**
   ```bash
   python -m app.ml.train
   ```

4. **Start the backend**
   ```bash
   python run.py
   ```
   The API will be available at `http://localhost:5000`

5. **Set up the frontend** (in a new terminal)
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   The frontend will be available at `http://localhost:3000`

### Environment Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Key environment variables:
- `SECRET_KEY` — Flask secret key (change in production)
- `DATABASE_URL` — Database connection string
- `MODEL_PATH` — Path to the trained model
- `CORS_ORIGINS` — Comma-separated allowed origins
- `MAX_MESSAGE_LENGTH` — Maximum message length (default: 5000)
- `MAX_BATCH_SIZE` — Maximum batch size (default: 100)

## API Endpoints

### Health & Metadata
- `GET /api/health` — Health check
- `GET /api/model/info` — Model version and metadata

### Prediction
- `POST /api/predict` — Classify a single message
- `POST /api/predict/batch` — Classify multiple messages

### History
- `GET /api/predictions` — Paginated prediction history
- `GET /api/predictions/<id>` — Get a single prediction
- `DELETE /api/predictions/<id>` — Delete a prediction
- `DELETE /api/predictions` — Clear all history
- `GET /api/predictions/export` — Export to CSV

### Analytics
- `GET /api/analytics/summary` — Summary statistics
- `GET /api/analytics/categories` — Category distribution
- `GET /api/analytics/trends` — Prediction trends

See [docs/api.md](docs/api.md) for detailed API documentation.

## Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Docker Deployment

### Using Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Individual Containers

```bash
# Build backend image
docker build -t fraud-detection-backend .

# Run backend
docker run -p 5000:5000 -v $(pwd)/model_artifacts:/app/model_artifacts fraud-detection-backend
```

## Dataset

**UCI SMS Spam Collection**
- 5,574 SMS messages labeled as 'spam' or 'ham' (legitimate)
- Public domain / CC0 license
- Source: [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/sms+spam+collection)

The dataset is automatically downloaded when you run the training script for the first time.

## Limitations

1. **Binary classification only**: The model classifies messages as spam or legitimate. It does NOT detect fraud or phishing specifically.
2. **SMS only**: Trained on SMS messages; may not generalize to emails or other formats.
3. **English only**: The model is trained on English-language messages.
4. **Not real-time**: Does not integrate with email or SMS providers.
5. **Educational purpose**: Designed for learning, not as a production security tool.

## Future Enhancements

- Multi-class classification with fraud and phishing detection
- Email and URL analysis capabilities
- Real-time API integration with email/SMS providers
- User authentication and personalized models
- Advanced explainability with SHAP values
- Mobile application

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

The UCI SMS Spam Collection dataset is available under CC0 1.0 Universal.

## Acknowledgments

- UCI Machine Learning Repository for the SMS Spam Collection dataset
- Scikit-learn documentation and community
- Flask and React communities
