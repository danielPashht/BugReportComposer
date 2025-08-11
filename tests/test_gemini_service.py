"""Smoke tests for the Gemini service."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import os
from src.core.exceptions import LLMServiceError
from src.services.gemini_service import GeminiService


class TestGeminiService:
    """Smoke tests for GeminiService."""

    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'})
    @patch('src.services.gemini_service.genai')
    def test_gemini_service_initialization(self, mock_genai):
        """Test that GeminiService can be initialized."""
        service = GeminiService()
        assert service is not None

    @patch('src.services.gemini_service.settings')
    def test_gemini_service_missing_api_key(self, mock_settings):
        """Test that GeminiService raises error without API key."""
        mock_settings.validate.side_effect = ValueError("GEMINI_API_KEY environment variable is required")

        with pytest.raises(ValueError, match="GEMINI_API_KEY environment variable is required"):
            GeminiService()

    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'})
    @patch('src.services.gemini_service.genai')
    def test_generate_bug_report_success(self, mock_genai):
        """Test successful bug report generation."""
        # Mock the generative model
        mock_model = MagicMock()
        mock_response = MagicMock()
        # Include all required fields for BugReportSchema with correct aliases
        mock_response.text = '''{"Title": "Test Bug", "Description of the issue": "Test description", "Steps": "1. Test step", "Expected result": "Expected", "Actual result": "Actual"}'''
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        service = GeminiService()
        result = service.generate_bug_report("Test user input")
        
        assert result is not None
        assert hasattr(result, 'title')
        assert result.title == "Test Bug"
        mock_model.generate_content.assert_called_once()

    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'})
    @patch('src.services.gemini_service.genai')
    def test_generate_bug_report_api_error(self, mock_genai):
        """Test handling of Gemini API errors."""
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_genai.GenerativeModel.return_value = mock_model
        
        service = GeminiService()
        
        with pytest.raises(LLMServiceError):
            service.generate_bug_report("Test user input")

    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'})
    @patch('src.services.gemini_service.genai')
    def test_generate_bug_report_invalid_json(self, mock_genai):
        """Test handling of invalid JSON response returns None."""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = 'Invalid JSON response'
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        service = GeminiService()
        result = service.generate_bug_report("Test user input")

        # The service returns None for invalid JSON after all retries fail
        assert result is None
