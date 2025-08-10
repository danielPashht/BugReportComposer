"""CLI interface for the Bug Reporter application."""

import sys
import argparse
from typing import Optional

from ..services import GeminiService, BugReportService
from ..formatters import JiraFormatter
from ..core.exceptions import BugReporterError


class CLI:
    """Command Line Interface for the Bug Reporter."""

    def __init__(self):
        """Initialize the CLI with default services."""
        self.llm_service = GeminiService()
        self.formatter = JiraFormatter()
        self.bug_report_service = BugReportService(self.llm_service, self.formatter)

    def create_parser(self) -> argparse.ArgumentParser:
        """Create and configure the argument parser."""
        parser = argparse.ArgumentParser(
            description="Convert user input to structured bug reports using Google Generative AI API",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
            Examples:
              python -m src.cli.main "App closes after clicking save button"
              python -m src.cli.main "Login form doesn't validate email addresses properly"
                        """,
        )

        parser.add_argument(
            "input_text", help="Description of the bug or issue to be formatted"
        )

        return parser

    def validate_input(self, input_text: str) -> bool:
        """
        Validate the input text.

        Args:
            input_text: The user's input

        Returns:
            True if valid, False otherwise
        """
        if not input_text.strip():
            print("Error: Input text cannot be empty.")
            return False
        return True

    def run(self, args: Optional[list] = None) -> None:
        """
        Run the CLI application.

        Args:
            args: Command line arguments (defaults to sys.argv)
        """
        parser = self.create_parser()

        try:
            parsed_args = parser.parse_args(args)
        except SystemExit:
            return

        # Validate input
        if not self.validate_input(parsed_args.input_text):
            sys.exit(1)

        # Process the bug report
        try:
            self.bug_report_service.process_bug_report(parsed_args.input_text)
        except BugReporterError as e:
            print(f"Error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)


def main():
    """Main entry point for the CLI application."""
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()
