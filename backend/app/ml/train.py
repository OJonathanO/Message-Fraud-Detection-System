"""Machine learning training pipeline.

Downloads the UCI SMS Spam Collection dataset, trains a TF-IDF +
Logistic Regression pipeline, evaluates on held-out test data,
and saves the trained model as a versioned artifact.

Dataset: UCI SMS Spam Collection
  - 5,574 SMS messages labeled as 'spam' or 'ham' (legitimate)
  - Public domain / CC0 license
  - Source: https://archive.ics.uci.edu/ml/datasets/sms+spam+collection

This is a BINARY classification task (spam vs. legitimate).
The system does NOT claim to detect fraud or phishing — those
categories require separate labeled datasets.
"""
import json
import logging
import os
import random
from datetime import datetime
from io import BytesIO
from typing import Any, Dict, Tuple
from zipfile import ZipFile

import joblib
import numpy as np
import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from .preprocessing import TextPreprocessor

logger = logging.getLogger(__name__)

# Dataset download URLs (tried in order)
DATASET_URLS = [
    "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip",
    "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv",
]

RANDOM_SEED = 42
TEST_SIZE = 0.2


def download_dataset(data_dir: str = "datasets") -> str:
    """Download the UCI SMS Spam Collection dataset.

    Args:
        data_dir: Directory to save the dataset.

    Returns:
        Path to the downloaded dataset file.

    Raises:
        RuntimeError: If the dataset cannot be downloaded from any source.
    """
    os.makedirs(data_dir, exist_ok=True)

    for url in DATASET_URLS:
        try:
            logger.info(f"Attempting to download dataset from {url}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            if url.endswith('.zip'):
                with ZipFile(BytesIO(response.content)) as zf:
                    zf.extractall(data_dir)
                # Find the extracted SMS file
                for fname in os.listdir(data_dir):
                    if fname.endswith('.txt') or fname.endswith('.tsv'):
                        return os.path.join(data_dir, fname)
            else:
                # Direct TSV download
                filepath = os.path.join(data_dir, 'sms_dataset.tsv')
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                return filepath

        except Exception as e:
            logger.warning(f"Failed to download from {url}: {e}")
            continue

    raise RuntimeError(
        "Could not download the dataset from any source. "
        "Please download it manually from "
        "https://archive.ics.uci.edu/ml/datasets/sms+spam+collection "
        "and place it in the datasets/ directory."
    )


def load_dataset(filepath: str) -> pd.DataFrame:
    """Load and validate the SMS dataset.

    Args:
        filepath: Path to the dataset file (TSV format).

    Returns:
        DataFrame with 'label' and 'message' columns.

    Raises:
        ValueError: If the dataset format is invalid.
    """
    # Try reading as TSV (UCI format: label\tmessage)
    try:
        df = pd.read_csv(filepath, sep='\t', header=None, names=['label', 'message'])
    except Exception:
        # Try with header
        df = pd.read_csv(filepath, sep='\t')

    # Validate required columns
    if 'label' not in df.columns or 'message' not in df.columns:
        raise ValueError(
            f"Dataset must have 'label' and 'message' columns. Found: {list(df.columns)}"
        )

    # Validate labels
    valid_labels = {'ham', 'spam'}
    actual_labels = set(df['label'].unique())
    if not actual_labels.issubset(valid_labels):
        raise ValueError(
            f"Dataset contains unexpected labels: {actual_labels}. "
            f"Expected subset of: {valid_labels}"
        )

    # Remove duplicates and missing values
    initial_count = len(df)
    df = df.drop_duplicates(subset=['message'])
    df = df.dropna(subset=['label', 'message'])
    df = df[df['message'].str.strip() != '']
    final_count = len(df)

    logger.info(f"Loaded {final_count} messages (removed {initial_count - final_count} duplicates/empty)")

    return df


def create_pipeline() -> Pipeline:
    """Create the TF-IDF + Logistic Regression pipeline.

    Returns:
        Scikit-learn Pipeline with preprocessing, vectorization, and classification.
    """
    pipeline = Pipeline([
        ('preprocessor', TextPreprocessor(remove_stop_words=False, lowercase=True)),
        ('tfidf', TfidfVectorizer(
            max_features=10000,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95,
            sublinear_tf=True,
        )),
        ('classifier', LogisticRegression(
            max_iter=1000,
            class_weight='balanced',
            random_state=RANDOM_SEED,
            C=1.0,
        )),
    ])

    return pipeline


def train_model(
    data_dir: str = "datasets",
    model_dir: str = "model_artifacts",
    download: bool = True,
) -> Dict[str, Any]:
    """Train the fraud detection model.

    Args:
        data_dir: Directory containing the dataset.
        model_dir: Directory to save model artifacts.
        download: Whether to download the dataset if not found.

    Returns:
        Dictionary containing evaluation metrics and metadata.
    """
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    os.makedirs(model_dir, exist_ok=True)

    # Find or download dataset
    dataset_path = None
    for fname in os.listdir(data_dir):
        if fname.endswith('.txt') or fname.endswith('.tsv'):
            dataset_path = os.path.join(data_dir, fname)
            break

    if dataset_path is None and download:
        dataset_path = download_dataset(data_dir)
    elif dataset_path is None:
        raise FileNotFoundError(
            f"No dataset found in {data_dir}. Run with download=True or "
            "download the dataset manually."
        )

    # Load and prepare data
    df = load_dataset(dataset_path)
    X = df['message'].values
    y = df['label'].values

    # Stratified train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_SEED, stratify=y
    )

    logger.info(f"Training set: {len(X_train)} samples")
    logger.info(f"Test set: {len(X_test)} samples")

    # Create and train pipeline
    pipeline = create_pipeline()
    logger.info("Training pipeline...")
    pipeline.fit(X_train, y_train)

    # Evaluate on test set
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, pos_label='spam')
    recall = recall_score(y_test, y_pred, pos_label='spam')
    f1 = f1_score(y_test, y_pred, pos_label='spam')

    # Per-class metrics
    class_report = classification_report(y_test, y_pred, output_dict=True)

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred, labels=['ham', 'spam'])

    # Build evaluation report
    evaluation = {
        'accuracy': round(accuracy, 4),
        'precision': round(precision, 4),
        'recall': round(recall, 4),
        'f1_score': round(f1, 4),
        'confusion_matrix': cm.tolist(),
        'confusion_matrix_labels': ['ham', 'spam'],
        'classification_report': class_report,
        'test_set_size': len(X_test),
        'train_set_size': len(X_train),
    }

    logger.info(f"Accuracy: {accuracy:.4f}")
    logger.info(f"Precision: {precision:.4f}")
    logger.info(f"Recall: {recall:.4f}")
    logger.info(f"F1 Score: {f1:.4f}")

    # Save model artifact
    model_path = os.path.join(model_dir, 'fraud_detection_model.joblib')
    joblib.dump(pipeline, model_path)
    logger.info(f"Model saved to {model_path}")

    # Save evaluation report
    eval_path = os.path.join(model_dir, 'evaluation_report.json')
    with open(eval_path, 'w') as f:
        json.dump(evaluation, f, indent=2)
    logger.info(f"Evaluation report saved to {eval_path}")

    # Save training metadata
    metadata = {
        'model_version': '1.0.0',
        'training_date': datetime.utcnow().isoformat(),
        'dataset': 'UCI SMS Spam Collection',
        'dataset_size': len(df),
        'train_size': len(X_train),
        'test_size': len(X_test),
        'random_seed': RANDOM_SEED,
        'test_split_ratio': TEST_SIZE,
        'pipeline_steps': [
            'TextPreprocessor (lowercase, entity normalization)',
            'TfidfVectorizer (max_features=10000, ngram_range=(1,2))',
            'LogisticRegression (class_weight=balanced, C=1.0)',
        ],
        'classification_type': 'binary',
        'classes': ['ham', 'spam'],
        'limitations': [
            'Binary classification only (spam vs. legitimate)',
            'Does NOT detect fraud or phishing — requires separate labeled datasets',
            'Trained on SMS messages only — may not generalize to emails or other formats',
            'Model performance depends on dataset quality and representativeness',
        ],
    }

    metadata_path = os.path.join(model_dir, 'training_metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    logger.info(f"Training metadata saved to {metadata_path}")

    return evaluation


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    train_model()
