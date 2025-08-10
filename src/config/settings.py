"""Configuration settings for the Bug Reporter application."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application configuration settings."""

    def __init__(self):
        """Initialize settings from environment variables."""
        self.gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
        self.gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        self.max_retries: int = int(os.getenv("MAX_RETRIES", "3"))

    def validate(self) -> bool:
        """Validate that required settings are present."""
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        return True


# Global settings instance
settings = Settings()
