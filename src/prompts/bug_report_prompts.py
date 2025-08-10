"""Prompts for the Bug Reporter application."""


class BugReportPrompts:
    """Container for bug report generation prompts."""

    @staticmethod
    def create_bug_report_prompt(user_input: str) -> str:
        """
        Create a strict prompt for the LLM to generate bug report JSON.

        Args:
            user_input: The user's bug description

        Returns:
            Formatted prompt for the LLM
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
