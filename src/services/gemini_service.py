"""Gemini AI service implementation."""
from typing import Optional
import google.generativeai as genai

from ..core.interfaces import LLMService
from ..core.models import BugReport, BugReportSchema
from ..core.exceptions import LLMServiceError
from ..config import settings
from ..prompts import BugReportPrompts


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
        Generate a structured bug report from user input using Gemini API with schema validation.

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
                    response_mime_type="application/json",
                    response_schema=BugReportSchema,
                    temperature=0.1,
                )

                model = genai.GenerativeModel(
                    self.model_name,
                    generation_config=generation_config
                )

                response = model.generate_content(prompt)

                try:
                    # Parse the structured response directly
                    bug_schema = BugReportSchema.model_validate_json(response.text.strip())
                    bug_report = BugReport.from_schema(bug_schema)

                    if (
                            bug_report.title.strip() and
                            bug_report.description.strip() and
                            bug_report.steps.strip()
                    ):
                        return bug_report
                    else:
                        print(f"Attempt {attempt + 1}: Generated bug report has empty fields, retrying...")
                        continue
                        
                except Exception as e:
                    print(f"Attempt {attempt + 1}: Schema validation failed - {e}")
                    if attempt == self.max_retries - 1:
                        print("Raw response that failed validation:")
                        print(response.text)
                    continue
                    
            except Exception as e:
                print(f"Attempt {attempt + 1}: API call failed - {e}")
                if attempt == self.max_retries - 1:
                    raise LLMServiceError(f"Failed to generate bug report after {self.max_retries} attempts: {e}")
                continue
        
        return None
