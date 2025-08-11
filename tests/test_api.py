"""Tests for the API endpoints."""

import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from src.api.app import app
from src.core.models import BugReport
from src.core.exceptions import BugReporterError


class TestBugReportAPI:
    """Tests for bug report API endpoints."""

    def setUp(self):
        """Set up test client."""
        self.client = TestClient(app)

    @patch("src.api.routes.GeminiService")
    @patch("src.api.routes.JiraFormatter")
    def test_bug_report_creation_success(self, mock_formatter_class, mock_gemini_class):
        """Test successful bug report creation via API."""
        # Setup mocks
        mock_gemini = Mock()
        mock_formatter = Mock()
        mock_gemini_class.return_value = mock_gemini
        mock_formatter_class.return_value = mock_formatter

        # Mock bug report
        mock_bug_report = BugReport(
            title="Test Bug",
            description="Test description",
            steps="1. Test step",
            expected_result="Expected result",
            actual_result="Actual result",
        )

        mock_gemini.generate_bug_report.return_value = mock_bug_report
        mock_formatter.format.return_value = "Formatted bug report"

        client = TestClient(app)

        response = client.post(
            "/api/v1/bug-reports", json={"user_input": "Test bug description"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Bug"
        assert data["description"] == "Test description"
        assert data["formatted_report"] == "Formatted bug report"

    @patch("src.api.routes.GeminiService")
    @patch("src.api.routes.JiraFormatter")
    def test_bug_report_gemini_service_error(
        self, mock_formatter_class, mock_gemini_class
    ):
        """Test API handling of Gemini service errors."""
        mock_gemini = Mock()
        mock_formatter = Mock()
        mock_gemini_class.return_value = mock_gemini
        mock_formatter_class.return_value = mock_formatter

        mock_gemini.generate_bug_report.side_effect = BugReporterError("Gemini error")

        client = TestClient(app)

        response = client.post(
            "/api/v1/bug-reports", json={"user_input": "Test bug description"}
        )

        assert response.status_code == 500
        assert "Bug report generation failed" in response.json()["detail"]

    @patch("src.api.routes.GeminiService")
    @patch("src.api.routes.JiraFormatter")
    def test_bug_report_gemini_returns_none(
        self, mock_formatter_class, mock_gemini_class
    ):
        """Test API handling when Gemini service returns None."""
        mock_gemini = Mock()
        mock_formatter = Mock()
        mock_gemini_class.return_value = mock_gemini
        mock_formatter_class.return_value = mock_formatter

        mock_gemini.generate_bug_report.return_value = None

        client = TestClient(app)

        response = client.post(
            "/api/v1/bug-reports", json={"user_input": "Test bug description"}
        )

        assert response.status_code == 500
        assert "Failed to generate bug report" in response.json()["detail"]

    @patch("src.api.routes.GeminiService")
    @patch("src.api.routes.JiraFormatter")
    def test_bug_report_formatter_error(self, mock_formatter_class, mock_gemini_class):
        """Test API handling of formatter errors."""
        mock_gemini = Mock()
        mock_formatter = Mock()
        mock_gemini_class.return_value = mock_gemini
        mock_formatter_class.return_value = mock_formatter

        mock_bug_report = BugReport(
            title="Test Bug",
            description="Test description",
            steps="1. Test step",
            expected_result="Expected result",
            actual_result="Actual result",
        )

        mock_gemini.generate_bug_report.return_value = mock_bug_report
        mock_formatter.format.side_effect = Exception("Formatter error")

        client = TestClient(app)

        response = client.post(
            "/api/v1/bug-reports", json={"user_input": "Test bug description"}
        )

        assert response.status_code == 500
        assert "An unexpected error occurred" in response.json()["detail"]

    def test_bug_report_invalid_request(self):
        """Test API handling of invalid request data."""
        client = TestClient(app)

        # Missing required field
        response = client.post("/api/v1/bug-reports", json={})

        assert response.status_code == 422  # Validation error

    @pytest.mark.skip(reason="Server not running on localhost:8000")
    def test_api_integration_with_server(self):
        """Test actual API integration (requires running server)."""
        # This test would require the actual server to be running
        # Skip for now as it's an integration test
        pass
