"""Tests for the machine learning pipeline."""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.ml.preprocessing import TextPreprocessor
from app.ml.train import create_pipeline, load_dataset


class TestPreprocessor:
    """Tests for the text preprocessor."""

    def test_url_normalization(self):
        """Test that URLs are normalized to URL token."""
        preprocessor = TextPreprocessor()
        result = preprocessor._preprocess("Check out https://example.com for deals")
        assert "URL" in result
        assert "https://example.com" not in result

    def test_email_normalization(self):
        """Test that emails are normalized to EMAIL token."""
        preprocessor = TextPreprocessor()
        result = preprocessor._preprocess("Contact me at test@example.com")
        assert "EMAIL" in result
        assert "test@example.com" not in result

    def test_phone_normalization(self):
        """Test that phone numbers are normalized to PHONE token."""
        preprocessor = TextPreprocessor()
        result = preprocessor._preprocess("Call me at 555-123-4567")
        assert "PHONE" in result

    def test_currency_normalization(self):
        """Test that currency amounts are normalized to MONEY token."""
        preprocessor = TextPreprocessor()
        result = preprocessor._preprocess("You won $1000!")
        assert "MONEY" in result

    def test_repeated_characters(self):
        """Test that repeated characters are collapsed."""
        preprocessor = TextPreprocessor()
        result = preprocessor._preprocess("Freeeee money!!!")
        assert "Free" in result or "free" in result

    def test_lowercase(self):
        """Test lowercasing."""
        preprocessor = TextPreprocessor(lowercase=True)
        result = preprocessor._preprocess("HELLO WORLD")
        assert result == result.lower()

    def test_whitespace_normalization(self):
        """Test that extra whitespace is removed."""
        preprocessor = TextPreprocessor()
        result = preprocessor._preprocess("  hello   world  ")
        assert result == "hello world"

    def test_empty_string(self):
        """Test handling of empty string."""
        preprocessor = TextPreprocessor()
        result = preprocessor._preprocess("")
        assert result == ""

    def test_non_string_input(self):
        """Test handling of non-string input."""
        preprocessor = TextPreprocessor()
        result = preprocessor._preprocess(123)
        assert isinstance(result, str)

    def test_fit_returns_self(self):
        """Test that fit returns self."""
        preprocessor = TextPreprocessor()
        result = preprocessor.fit(["test"])
        assert result is preprocessor

    def test_transform_list(self):
        """Test transforming a list of texts."""
        preprocessor = TextPreprocessor()
        result = preprocessor.transform(["Hello world", "Test message"])
        assert len(result) == 2
        assert all(isinstance(r, str) for r in result)


class TestPipeline:
    """Tests for the ML pipeline."""

    def test_pipeline_creation(self):
        """Test that pipeline can be created."""
        pipeline = create_pipeline()
        assert pipeline is not None
        assert hasattr(pipeline, 'predict')
        assert hasattr(pipeline, 'fit')

    def test_pipeline_steps(self):
        """Test that pipeline has correct steps."""
        pipeline = create_pipeline()
        step_names = [name for name, _ in pipeline.steps]
        assert 'preprocessor' in step_names
        assert 'tfidf' in step_names
        assert 'classifier' in step_names


class TestDatasetLoading:
    """Tests for dataset loading."""

    def test_load_dataset_invalid_path(self):
        """Test loading from non-existent path raises error."""
        with pytest.raises((FileNotFoundError, Exception)):
            load_dataset("nonexistent_file.tsv")
