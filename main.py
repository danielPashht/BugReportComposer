#!/usr/bin/env python3
"""
Bug Reporter - A Python console app that converts user input to structured bug reports
using Google Generative AI's API and formats them for Jira.
"""

import sys
import os
import json
import argparse
from typing import Dict, Any, Optional
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env

gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)


class BugReporter:
    """Main class for handling bug report generation and formatting."""

    def __init__(self):
        """Initialize the BugReporter."""
        self.model = "gemini-1.5-flash"  # Free tier model

        # Required JSON structure
        self.required_fields = [
            "Title",
            "Description of the issue",
            "Steps",
            "Expected result",
            "Actual result"
        ]

    @staticmethod
    def create_prompt(user_input: str) -> str:
        """
        Create a strict prompt for the LLM to generate bug report JSON.

        Args:
            user_input (str): The user's bug description

        Returns:
            str: Formatted prompt for the LLM
        """
        return f"""You are a bug report formatter.
                You must respond ONLY with valid JSON in the following structure:
                {{
                  "Title": "string",
                  "Description of the issue": "string",
                  "Steps": "string",
                  "Expected result": "string",
                  "Actual result": "string"
                }}
                Do not include any text outside JSON.

                User input: {user_input}
                Ensure all fields are present and are strings.
                If any field is missing or not a string, return an error message in JSON format."""

    def call_gemini_api(self, user_input: str, max_retries: int = 3) -> Optional[Dict[str, Any]]:
        """
        Call Gemini API to generate bug report JSON.

        Args:
            user_input (str): The user's bug description
            max_retries (int): Maximum number of retry attempts

        Returns:
            Optional[Dict[str, Any]]: Parsed JSON response or None if failed
        """
        prompt = self.create_prompt(user_input)

        for attempt in range(max_retries):
            try:
                response = genai.GenerativeModel(self.model).generate_content(prompt)

                content = response.text.strip()

                # Clean up potential markdown code block
                if content.startswith("```json"):
                    content = content.removeprefix("```json").strip()
                if content.endswith("```"):
                    content = content.removesuffix("```").strip()

                # Try to parse JSON
                try:
                    bug_report = json.loads(content)

                    # Validate required fields
                    if self.validate_json_structure(bug_report):
                        return bug_report
                    else:
                        print(f"Attempt {attempt + 1}: Invalid JSON structure, retrying...")
                        continue

                except json.JSONDecodeError as e:
                    print(f"Attempt {attempt + 1}: JSON parsing failed - {e}")
                    if attempt == max_retries - 1:
                        print("Raw response that failed to parse:")
                        print(content)
                    continue

            except Exception as e:
                print(f"Attempt {attempt + 1}: API call failed - {e}")
                if attempt == max_retries - 1:
                    print("All retry attempts exhausted.")
                    return None
                continue

        return None

    def validate_json_structure(self, data: Dict[str, Any]) -> bool:
        """
        Validate that the JSON contains all required fields.

        Args:
            data (Dict[str, Any]): The JSON data to validate

        Returns:
            bool: True if valid structure, False otherwise
        """
        if not isinstance(data, dict):
            return False

        for field in self.required_fields:
            if field not in data:
                print(f"Missing required field: {field}")
                return False
            if not isinstance(data[field], str):
                print(f"Field '{field}' must be a string")
                return False

        return True

    @staticmethod
    def format_for_jira(bug_report: Dict[str, Any]) -> str:
        """
        Format the bug report JSON into a Jira-friendly text format.

        Args:
            bug_report (Dict[str, Any]): The original bug report JSON

        Returns:
            str: A formatted string ready to be pasted into Jira.
        """
        jira_text = []
        for key, value in bug_report.items():
            # Using Jira's markup for bold
            jira_text.append(f"*{key}*:\n{value}")
        return "\n\n".join(jira_text)

    def process_bug_report(self, user_input: str) -> None:
        """
        Main processing function that handles the entire workflow.

        Args:
            user_input (str): The user's bug description
        """
        print("Generating bug report...")

        # Get JSON from Gemini
        bug_report = self.call_gemini_api(user_input)

        if bug_report is None:
            print("Failed to generate bug report. Please try again.")
            sys.exit(1)

        # Format for Jira
        formatted_report = self.format_for_jira(bug_report)

        print("\n--- JIRA BUG REPORT ---")
        print(formatted_report)
        print("-----------------------")


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description="Convert user input to structured bug reports using Google Generative AI API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Examples:
          python main.py "App closes after clicking save button"
          python main.py "Login form doesn't validate email addresses properly"
                """
    )

    parser.add_argument(
        "input_text",
        help="Description of the bug or issue to be formatted"
    )

    # Parse arguments
    try:
        args = parser.parse_args()
    except SystemExit:
        return

    # Validate input
    if not args.input_text.strip():
        print("Error: Input text cannot be empty.")
        sys.exit(1)

    # Process the bug report
    reporter = BugReporter()
    reporter.process_bug_report(args.input_text)


if __name__ == "__main__":
    main()
