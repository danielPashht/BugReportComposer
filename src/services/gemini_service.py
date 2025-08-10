"""Gemini AI service implementation."""
import json
from typing import Optional
import google.generativeai as genai

from ..core.interfaces import LLMService
from ..core.models import BugReport
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
        Generate a structured bug report from user input using Gemini API.
        
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
                response = genai.GenerativeModel(self.model_name).generate_content(prompt)
                content = response.text.strip()
                
                # Clean up potential markdown code block
                if content.startswith("```json"):
                    content = content.removeprefix("```json").strip()
                if content.endswith("```"):
                    content = content.removesuffix("```").strip()
                
                # Parse JSON and create BugReport
                try:
                    bug_data = json.loads(content)
                    bug_report = BugReport.from_dict(bug_data)
                    
                    # Validate the bug report
                    if bug_report.validate():
                        return bug_report
                    else:
                        print(f"Attempt {attempt + 1}: Invalid bug report structure, retrying...")
                        continue
                        
                except json.JSONDecodeError as e:
                    print(f"Attempt {attempt + 1}: JSON parsing failed - {e}")
                    if attempt == self.max_retries - 1:
                        print("Raw response that failed to parse:")
                        print(content)
                    continue
                    
            except Exception as e:
                print(f"Attempt {attempt + 1}: API call failed - {e}")
                if attempt == self.max_retries - 1:
                    raise LLMServiceError(f"Failed to generate bug report after {self.max_retries} attempts: {e}")
                continue
        
        return None
