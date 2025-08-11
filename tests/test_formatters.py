"""Smoke tests for formatters."""

import pytest
from src.formatters.jira_formatter import JiraFormatter
from src.formatters.base_formatter import BaseFormatter
from src.core.models import BugReport


class TestJiraFormatter:
    """Smoke tests for JiraFormatter."""

    def test_jira_formatter_initialization(self):
        """Test that JiraFormatter can be initialized."""
        formatter = JiraFormatter()
        assert formatter is not None
        assert isinstance(formatter, BaseFormatter)

    def test_jira_formatter_format_bug_report(self):
        """Test JiraFormatter can format a bug report."""
        formatter = JiraFormatter()
        bug_report = BugReport(
            title="Test Bug",
            description="Test description",
            steps="1. Step one\n2. Step two",
            expected_result="Expected result",
            actual_result="Actual result",
        )

        formatted = formatter.format(bug_report)

        assert isinstance(formatted, str)
        assert len(formatted) > 0
        assert "Test Bug" in formatted
        assert "Step one" in formatted
        assert "Step two" in formatted

    def test_jira_formatter_empty_steps(self):
        """Test JiraFormatter handles empty steps."""
        formatter = JiraFormatter()
        bug_report = BugReport(
            title="Test Bug",
            description="Test description",
            steps="",
            expected_result="Expected result",
            actual_result="Actual result",
        )

        formatted = formatter.format(bug_report)
        assert isinstance(formatted, str)
        assert "Test Bug" in formatted

    def test_jira_formatter_special_characters(self):
        """Test JiraFormatter handles special characters."""
        formatter = JiraFormatter()
        bug_report = BugReport(
            title="Test Bug with *special* characters",
            description="Description with [brackets] and {braces}",
            steps="1. Step with | pipe\n2. Step with _ underscore",
            expected_result="Expected with ~ tilde",
            actual_result="Actual with ^ caret",
        )

        formatted = formatter.format(bug_report)
        assert isinstance(formatted, str)
        assert len(formatted) > 0


class TestBaseFormatter:
    """Smoke tests for BaseFormatter."""

    def test_base_formatter_is_abstract(self):
        """Test that BaseFormatter cannot be instantiated directly."""
        with pytest.raises(TypeError):
            BaseFormatter()

    def test_base_formatter_subclass_must_implement_format(self):
        """Test that BaseFormatter subclasses must implement format method."""

        class IncompleteFormatter(BaseFormatter):
            pass

        with pytest.raises(TypeError):
            IncompleteFormatter()

    def test_base_formatter_valid_subclass(self):
        """Test that valid BaseFormatter subclass can be created."""

        class ValidFormatter(BaseFormatter):
            def format(self, bug_report):
                return "formatted"

        formatter = ValidFormatter()
        assert formatter is not None
        assert formatter.format(None) == "formatted"
