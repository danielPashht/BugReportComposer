"""Main bug report service that orchestrates the business logic."""

from typing import Optional

from ..core.interfaces import LLMService, Formatter
from ..core.models import BugReport
from ..core.exceptions import BugReporterError


class BugReportService:
    """Main service for generating and formatting bug reports."""

    def __init__(self, llm_service: LLMService, formatter: Formatter):
        """
        Initialize the bug report service.

        Args:
            llm_service: LLM service implementation
            formatter: Formatter implementation
        """
        self.llm_service = llm_service
        self.formatter = formatter

    def generate_formatted_report(self, user_input: str) -> Optional[str]:
        """
        Generate a bug report and format it for the target platform.

        Args:
            user_input: The user's description of the bug

        Returns:
            Formatted bug report string or None if generation failed

        Raises:
            BugReporterError: If the process fails
        """
        try:
            bug_report: BugReport = self.llm_service.generate_bug_report(user_input)

            if bug_report is None:
                return None
            formatted_report = self.formatter.format(bug_report)

            return formatted_report

        except Exception as e:
            raise BugReporterError(f"Failed to generate formatted report: {e}")

    def process_bug_report(self, user_input: str) -> None:
        """
        Process a bug report and print the results.

        Args:
            user_input: The user's description of the bug
        """
        print("Generating bug report...")

        try:
            formatted_report = self.generate_formatted_report(user_input)

            if formatted_report is None:
                print("Failed to generate bug report. Please try again.")
                return

            print("\n--- FORMATTED BUG REPORT ---")
            print(formatted_report)
            print("---------------------------")

        except BugReporterError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
