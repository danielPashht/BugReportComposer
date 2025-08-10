#!/usr/bin/env python3
"""
Bug Reporter - A Python console app that converts user input to structured bug reports
using Google Generative AI's API and formats them for Jira.
"""

import sys
import argparse
from src.services.gemini_service import GeminiService
from src.services.bug_report_service import BugReportService
from src.formatters.jira_formatter import JiraFormatter
from src.core.exceptions import BugReporterError


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description="Convert user input to structured bug reports using AI API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Examples:
          python main.py "App closes after clicking save button"
          python main.py "Login form doesn't validate email addresses properly"
                """,
    )

    parser.add_argument(
        "input_text", help="Description of the bug or issue to be formatted"
    )

    try:
        args = parser.parse_args()
    except SystemExit:
        return

    if not args.input_text.strip():
        print("Error: Input text cannot be empty.")
        sys.exit(1)

    try:
        llm_service = GeminiService()
        formatter = JiraFormatter()
        bug_service = BugReportService(llm_service, formatter)

        bug_service.process_bug_report(args.input_text)

    except BugReporterError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
