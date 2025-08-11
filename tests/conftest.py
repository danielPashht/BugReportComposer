"""Pytest configuration and shared fixtures."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from src.api.app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_gemini_service():
    """Mock the Gemini service for testing."""
    with patch("src.services.gemini_service.GeminiService") as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance

        # Mock a successful response
        mock_instance.generate_bug_report.return_value = {
            "title": "Test Bug Title",
            "description": "Test bug description",
            "steps": "1. Open page\n2. Look for header",
            "expected_result": "Header should be visible",
            "actual_result": "Header is missing, 404 error in console",
        }
        yield mock_instance


@pytest.fixture
def sample_bug_report_request():
    """Sample bug report request data."""
    return {
        "user_input": "there is no header displayed on the main page, i can see error 404 in js console"
    }


@pytest.fixture
def sample_bug_report_response():
    """Sample bug report response data."""
    return {
        "title": "Missing Header on Main Page with 404 Console Error",
        "description": "The main page is not displaying the header element, and there is a 404 error visible in the JavaScript console.",
        "steps": "1. Navigate to the main page\n2. Observe the header area\n3. Open browser developer tools\n4. Check the console tab",
        "expected_result": "Header should be visible on the main page with no console errors",
        "actual_result": "Header is missing and 404 error appears in console",
        "severity": "medium",
        "priority": "high",
        "formatted_report": "**Bug Report**\n\n**Title:** Missing Header on Main Page with 404 Console Error\n...",
    }
