"""Prompts for the Bug Reporter application."""


class BugReportPrompts:
    """Container for bug report generation prompts."""

    @staticmethod
    def create_bug_report_prompt(user_input: str) -> str:
        """
        Args:
            user_input: The user's bug description

        Returns:
            Formatted prompt for the LLM
        """
        return f"""You are a bug report formatter. Analyze the following user input and create a structured bug report.

                User input: {user_input}
                
                Provide:
                - A clear, concise title for the bug
                - A detailed description of the issue
                - Step-by-step reproduction instructions, start with an action verb, and be testable actions.
                - What the user expected to happen
                - What actually happened
                
                Focus on clarity and completeness. 
                Rewrite vague steps into explicit actions (only if it possible without additional context).
                """
