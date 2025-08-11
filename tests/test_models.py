"""Smoke tests for models and schemas."""

import pytest
from pydantic import ValidationError
from src.api.models import BugReportRequest, BugReportResponse
from src.core.models import BugReport


class TestBugReportSchemas:
    """Smoke tests for bug report schemas."""

    def test_bug_report_request_valid(self):
        """Test valid bug report request creation."""
        request = BugReportRequest(user_input="Test bug description")
        assert request.user_input == "Test bug description"

    def test_bug_report_request_empty_input(self):
        """Test bug report request with empty input."""
        with pytest.raises(ValidationError):
            BugReportRequest(user_input="")

    def test_bug_report_request_missing_input(self):
        """Test bug report request with missing input."""
        with pytest.raises(ValidationError):
            BugReportRequest()

    def test_bug_report_response_valid(self):
        """Test valid bug report response creation."""
        response = BugReportResponse(
            title="Test Bug",
            description="Test description",
            steps="1. Step one\n2. Step two",
            expected_result="Expected result",
            actual_result="Actual result",
            formatted_report="Formatted report text",
        )

        assert response.title == "Test Bug"
        assert response.description == "Test description"
        assert response.formatted_report == "Formatted report text"

    def test_bug_report_response_missing_required_fields(self):
        """Test bug report response with missing required fields."""
        with pytest.raises(ValidationError):
            BugReportResponse(title="Test Bug")


class TestBugReportModel:
    """Smoke tests for BugReport core model."""

    def test_bug_report_model_creation(self):
        """Test BugReport model creation."""
        bug_report = BugReport(
            title="Test Bug",
            description="Test description",
            steps="1. Step one\n2. Step two",
            expected_result="Expected",
            actual_result="Actual",
        )

        assert bug_report.title == "Test Bug"
        assert bug_report.description == "Test description"
        assert bug_report.steps == "1. Step one\n2. Step two"

    def test_bug_report_to_dict(self):
        """Test BugReport model to_dict method."""
        bug_report = BugReport(
            title="Test Bug",
            description="Test description",
            steps="1. Step one",
            expected_result="Expected",
            actual_result="Actual",
        )

        result = bug_report.to_dict()
        assert isinstance(result, dict)
        assert result["Title"] == "Test Bug"
        assert result["Description of the issue"] == "Test description"
