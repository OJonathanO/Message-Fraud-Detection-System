"""Text preprocessing module for NLP pipeline.

This module provides a scikit-learn compatible transformer for text
normalization. It handles URL/email/phone/currency normalization,
repeated character collapsing, and optional stop-word removal.

Important: URLs, currency symbols, phone numbers, and numeric patterns
are NOT removed. Instead, they are normalized to special tokens (URL,
EMAIL, PHONE, MONEY, NUM) so the TF-IDF vectorizer can learn their
predictive value for fraud detection.
"""
import re
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


class TextPreprocessor(BaseEstimator, TransformerMixin):
    """Scikit-learn compatible text preprocessor.

    Normalizes text for TF-IDF feature extraction while preserving
    fraud-relevant indicators as special tokens.
    """

    # Regex patterns for entity normalization
    URL_PATTERN = re.compile(r'http[s]?://\S+|www\.\S+', re.IGNORECASE)
    EMAIL_PATTERN = re.compile(r'\S+@\S+\.\S+', re.IGNORECASE)
    PHONE_PATTERN = re.compile(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')
    CURRENCY_PATTERN = re.compile(r'[$£€¥]\s*\d+(?:,\d{3})*(?:\.\d+)?|\d+(?:,\d{3})*(?:\.\d+)?\s*(?:USD|EUR|GBP|dollars?|euros?|pounds?)', re.IGNORECASE)
    NUMBER_PATTERN = re.compile(r'\b\d+\b')
    REPEATED_CHAR_PATTERN = re.compile(r'(.)\1{2,}')
    WHITESPACE_PATTERN = re.compile(r'\s+')

    def __init__(self, remove_stop_words: bool = False, lowercase: bool = True):
        """Initialize the preprocessor.

        Args:
            remove_stop_words: Whether to remove English stop words.
                Defaults to False because words like 'your', 'account',
                'verify' are important fraud indicators.
            lowercase: Whether to convert text to lowercase.
        """
        self.remove_stop_words = remove_stop_words
        self.lowercase = lowercase

    def fit(self, X, y=None):
        """Fit the transformer (no-op, returns self)."""
        return self

    def transform(self, X):
        """Transform a list of text strings.

        Args:
            X: Iterable of text strings.

        Returns:
            List of preprocessed text strings.
        """
        return [self._preprocess(text) for text in X]

    def _preprocess(self, text: str) -> str:
        """Apply all preprocessing steps to a single text string.

        Args:
            text: Raw input text.

        Returns:
            Preprocessed text string.
        """
        if not isinstance(text, str):
            text = str(text)

        if self.lowercase:
            text = text.lower()

        # Normalize entities to special tokens (preserve predictive value)
        text = self.URL_PATTERN.sub(' URL ', text)
        text = self.EMAIL_PATTERN.sub(' EMAIL ', text)
        text = self.PHONE_PATTERN.sub(' PHONE ', text)
        text = self.CURRENCY_PATTERN.sub(' MONEY ', text)
        text = self.NUMBER_PATTERN.sub(' NUM ', text)

        # Collapse repeated characters (e.g., "freeee" -> "free")
        text = self.REPEATED_CHAR_PATTERN.sub(r'\1\1', text)

        # Normalize whitespace
        text = self.WHITESPACE_PATTERN.sub(' ', text).strip()

        # Optional stop word removal
        if self.remove_stop_words:
            words = text.split()
            words = [w for w in words if w not in ENGLISH_STOP_WORDS]
            text = ' '.join(words)

        return text
