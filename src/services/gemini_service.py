"""Gemini AI service implementation."""

from typing import Optional
import json
import google.generativeai as genai
from pydantic import ValidationError

from ..core.interfaces import LLMService
from ..core.models import BugReport
from ..core.exceptions import LLMServiceError
from ..config import settings
from ..prompts import BugReportPrompts
from ..schemas.bug_report import BugReportSchema


class GeminiService(LLMService):
    """Gemini AI implementation of the LLM service."""

    def __init__(self):
        """Initialize the Gemini service."""
        settings.validate()
        genai.configure(api_key=settings.gemini_api_key)
        self.model_name = settings.gemini_model
        self.max_retries = settings.max_retries

    def generate_bug_report(self, user_input: str) -> Optional[BugReport]:
        """
        Generate a structured bug report from user input using Gemini API with JSON parsing.

        Args:
            user_input: The user's description of the bug

        Returns:
            BugReport instance or None if generation failed

        Raises:
            LLMServiceError: If API calls fail after all retries
        """
        prompt = BugReportPrompts.create_bug_report_prompt(user_input)

        for attempt in range(self.max_retries):
            try:
                generation_config = genai.GenerationConfig(
                    temperature=0.1,
                )

                model = genai.GenerativeModel(
                    self.model_name, generation_config=generation_config
                )

                response = model.generate_content(prompt)

                try:
                    # Parse the JSON response
                    response_text = response.text.strip()

                    # Remove any markdown code block markers if present
                    if response_text.startswith("```json"):
                        response_text = response_text[7:]
                    if response_text.endswith("```"):
                        response_text = response_text[:-3]

                    response_text = response_text.strip()

                    data = json.loads(response_text)

                    validated_data = BugReportSchema(**data)

                    bug_report = BugReport(
                        title=validated_data.title,
                        description=validated_data.description_of_the_issue,
                        steps=validated_data.steps,
                        expected_result=validated_data.expected_result,
                        actual_result=validated_data.actual_result,
                    )

                    if (
                        bug_report.title.strip()
                        and bug_report.description.strip()
                        and bug_report.steps.strip()
                    ):
                        return bug_report
                    else:
                        print(
                            f"Attempt {attempt + 1}: Generated bug report has empty fields, retrying..."
                        )
                        continue

                except (json.JSONDecodeError, ValidationError) as e:
                    print(f"Attempt {attempt + 1}: Schema validation failed - {e}")
                    if attempt == self.max_retries - 1:
                        print("Raw response that failed parsing:")
                        print(response.text)
                    continue

            except Exception as e:
                print(f"Attempt {attempt + 1}: API call failed - {e}")
                if attempt == self.max_retries - 1:
                    raise LLMServiceError(
                        f"Failed to generate bug report after {self.max_retries} attempts: {e}"
                    )
                continue

        return None
