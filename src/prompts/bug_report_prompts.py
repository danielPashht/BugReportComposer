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
        return f"""You are a bug report generator.
                You must respond ONLY with valid JSON in the following structure:
                {{
                  "Title": "string",
                  "Description of the issue": "string", 
                  "Steps": "string",
                  "Expected result": "string",
                  "Actual result": "string"
                }}
                DO NOT include any text outside JSON!
                FORMAT RULES:
                1. Ensure all fields are present and are strings.
                2. If any field is missing or not a string, return an error message in JSON format.
                STYLE RULES:
                1. Title should be brief, concise and 20-50 characters length 
                2. Focus on clarity and completeness. If any information is missing from the user input, 
                make reasonable assumptions or indicate where information might be incomplete.
                3. Use concise language, avoid unnecessary details.
                4. 
                
                User input: {user_input}
                """
