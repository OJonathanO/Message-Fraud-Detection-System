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
