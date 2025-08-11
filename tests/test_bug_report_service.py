"""Tests for the bug report service."""

import pytest
from unittest.mock import Mock, MagicMock
from src.services.bug_report_service import BugReportService
from src.core.exceptions import BugReporterError
from src.core.models import BugReport


class TestBugReportService:
    """Tests for BugReportService with dependency injection."""

    def test_bug_report_service_initialization(self):
        """Test that BugReportService can be initialized with dependencies."""
        mock_llm_service = Mock()
        mock_formatter = Mock()

        service = BugReportService(mock_llm_service, mock_formatter)

        assert service is not None
        assert service.llm_service == mock_llm_service
        assert service.formatter == mock_formatter

    def test_generate_formatted_report_success(self):
        """Test successful bug report generation and formatting."""
        # Setup mocks
        mock_llm_service = Mock()
        mock_formatter = Mock()

        # Mock bug report
        mock_bug_report = BugReport(
            title="Test Bug",
            description="Test description",
            steps="1. Test step",
            expected_result="Expected result",
            actual_result="Actual result",
        )

        mock_llm_service.generate_bug_report.return_value = mock_bug_report
        mock_formatter.format.return_value = "Formatted bug report"

        service = BugReportService(mock_llm_service, mock_formatter)
        result = service.generate_formatted_report("Test user input")

        assert result == "Formatted bug report"
        mock_llm_service.generate_bug_report.assert_called_once_with("Test user input")
        mock_formatter.format.assert_called_once_with(mock_bug_report)

    def test_generate_formatted_report_llm_returns_none(self):
        """Test handling when LLM service returns None."""
        mock_llm_service = Mock()
        mock_formatter = Mock()

        mock_llm_service.generate_bug_report.return_value = None

        service = BugReportService(mock_llm_service, mock_formatter)
        result = service.generate_formatted_report("Test user input")

        assert result is None
        mock_llm_service.generate_bug_report.assert_called_once_with("Test user input")
        mock_formatter.format.assert_not_called()

    def test_generate_formatted_report_llm_service_error(self):
        """Test handling of LLM service errors."""
        mock_llm_service = Mock()
        mock_formatter = Mock()

        mock_llm_service.generate_bug_report.side_effect = Exception("LLM Error")

        service = BugReportService(mock_llm_service, mock_formatter)

        with pytest.raises(
            BugReporterError, match="Failed to generate formatted report"
        ):
            service.generate_formatted_report("Test user input")

    def test_generate_formatted_report_formatter_error(self):
        """Test handling of formatter errors."""
        mock_llm_service = Mock()
        mock_formatter = Mock()

        mock_bug_report = BugReport(
            title="Test Bug",
            description="Test description",
            steps="1. Test step",
            expected_result="Expected result",
            actual_result="Actual result",
        )

        mock_llm_service.generate_bug_report.return_value = mock_bug_report
        mock_formatter.format.side_effect = Exception("Formatter Error")

        service = BugReportService(mock_llm_service, mock_formatter)

        with pytest.raises(
            BugReporterError, match="Failed to generate formatted report"
        ):
            service.generate_formatted_report("Test user input")
