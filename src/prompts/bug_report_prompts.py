"""Prompts for the Bug Reporter application."""


class BugReportPrompts:
    """Container for bug report generation prompts."""

    @staticmethod
    def create_bug_report_prompt(user_input: str) -> str:
        """
        Create a prompt for the LLM to generate bug report data.

        Args:
            user_input: The user's bug description

        Returns:
            Formatted prompt for the LLM
        """
        return f"""You are a bug report formatter. Analyze the following user input and create a structured bug report.

User input: {user_input}

Please provide:
- A clear, concise title for the bug
- A detailed description of the issue
- Step-by-step reproduction instructions
- What the user expected to happen
- What actually happened

Focus on clarity and completeness. If any information is missing from the user input, make reasonable assumptions or indicate where information might be incomplete."""
