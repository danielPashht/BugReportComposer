"""Jira-specific formatter implementation."""

from ..core.models import BugReport
from .base_formatter import BaseFormatter


class JiraFormatter(BaseFormatter):
    """Formatter for Jira bug tracking system."""

    def format(self, bug_report: BugReport) -> str:
        """
        Format the bug report for Jira using Jira markup.

        Args:
            bug_report: The bug report to format

        Returns:
            Jira-formatted string ready to be pasted into Jira
        """
        formatted_sections = []
        bug_dict = bug_report.to_dict()

        for label, value in bug_dict.items():
            # Ensure value is properly encoded and split into lines for multi-language text
            if isinstance(value, str) and label.lower() == "steps":
                value = value.replace('\n', '\n')
                value = value.replace('\n', '\n\n')  # Add extra newline for better rendering

            # Using Jira's markup for bold text
            formatted_section = self._format_jira_field(label, value)
            formatted_sections.append(formatted_section)

        return "\n\n".join(formatted_sections)

    @staticmethod
    def _format_jira_field(label: str, value: str) -> str:
        """
        Format a field specifically for Jira.

        Args:
            label: Field label
            value: Field value

        Returns:
            Jira-formatted field string
        """
        return f"*{label}*:\n{value}"
