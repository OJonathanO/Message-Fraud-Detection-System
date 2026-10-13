# Architecture Documentation

## System Overview

The Message Fraud Detection System follows a client-server architecture with clear separation of concerns:

- **Frontend**: React SPA handling user interaction and data visualization
- **Backend**: Flask REST API handling business logic and ML inference
- **Database**: SQLite for persistent storage (PostgreSQL-ready)

## Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        React Frontend                            │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │Dashboard │  │ Analyzer │  │ History  │  │Model Perform.│   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └──────┬───────┘   │
│       │              │              │               │           │
│       └──────────────┴──────────────┴───────────────┘           │
│                           │                                      │
│                    ┌──────▼──────┐                               │
│                    │  API Client │                               │
│                    │  (Axios)    │                               │
│                    └──────┬──────┘                               │
└───────────────────────────┼─────────────────────────────────────┘
                            │ HTTP/JSON
┌───────────────────────────▼─────────────────────────────────────┐
│                        Flask Backend                             │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Blueprints                            │    │
│  │  ┌─────────┐  ┌──────────┐  ┌─────────┐  ┌──────────┐  │    │
│  │  │ Health  │  │ Predict  │  │ History │  │Analytics │  │    │
│  │  └────┬────┘  └────┬─────┘  └────┬────┘  └────┬─────┘  │    │
│  └───────┼─────────────┼─────────────┼─────────────┼────────┘    │
│          │             │             │             │              │
│  ┌───────▼─────────────▼─────────────▼─────────────▼────────┐    │
│  │                  Service Layer                           │    │
│  │  ┌──────────────────────────────────────────────────┐   │    │
│  │  │           Prediction Service                      │   │    │
│  │  │  - Risk assessment                                │   │    │
│  │  │  - Indicator generation                           │   │    │
│  │  │  - Recommendation building                        │   │    │
│  │  └──────────────────────────────────────────────────┘   │    │
│  └──────────────────────────┬───────────────────────────────┘    │
│                             │                                    │
│  ┌──────────────────────────▼───────────────────────────────┐    │
│  │                    ML Pipeline                           │    │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────────┐   │    │
│  │  │Preprocessor│→│  TF-IDF    │→│ Logistic Regress.│   │    │
│  │  │(normalize) │  │(vectorize) │  │ (classify)       │   │    │
│  │  └────────────┘  └────────────┘  └──────────────────┘   │    │
│  └──────────────────────────────────────────────────────────┘    │
│                             │                                    │
│  ┌──────────────────────────▼───────────────────────────────┐    │
│  │              Data Layer (SQLAlchemy)                      │    │
│  │  ┌────────────────────────────────────────────────┐      │    │
│  │  │              predictions table                  │      │    │
│  │  └────────────────────────────────────────────────┘      │    │
│  └──────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────┘
```

## Data Flow

1. **User submits message** → React frontend sends POST request to `/api/predict`
2. **Input validation** → Flask validates message length and content
3. **ML inference** → Message passes through preprocessing → TF-IDF → Logistic Regression
4. **Risk assessment** → Service layer calculates risk level based on class and confidence
5. **Explanation** → Explainability engine extracts influential terms
6. **Persistence** → Prediction stored in SQLite database
7. **Response** → JSON response returned to frontend
8. **Display** → React renders prediction result with indicators and recommendation

## Design Decisions

### Why TF-IDF + Logistic Regression?

- **Interpretable**: Coefficients directly show feature importance
- **Fast**: Predictions in milliseconds
- **Effective**: Strong baseline for text classification
- **Simple**: Easy to explain in interviews

### Why a Scikit-learn Pipeline?

- **Consistency**: Same transformations during training and inference
- **No data leakage**: Vectorizer fit only on training data
- **Reproducible**: Fixed random seed ensures same results
- **Maintainable**: Single artifact contains all preprocessing

### Why SQLite?

- **Zero configuration**: No separate database server needed
- **Portable**: Single file database
- **PostgreSQL-ready**: SQLAlchemy abstraction allows easy migration

### Why Application Factory Pattern?

- **Testability**: Easy to create app instances with different configs
- **Modularity**: Blueprints can be registered conditionally
- **Flexibility**: Multiple app instances for testing

## Security Considerations

- Input validation on all user-supplied data
- Message length limits prevent abuse
- Rate limiting prevents API abuse
- CORS restricted to configured origins
- CSV formula injection protection
- No secrets in source code (environment variables)
- Parameterized queries via SQLAlchemy ORM
