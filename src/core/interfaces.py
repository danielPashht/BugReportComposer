"""Abstract interfaces for the Bug Reporter application."""

from abc import ABC, abstractmethod
from typing import Optional
from .models import BugReport


class LLMService(ABC):
    """Abstract interface for LLM services."""

    @abstractmethod
    def generate_bug_report(self, user_input: str) -> Optional[BugReport]:
        """
        Generate a structured bug report from user input.

        Args:
            user_input: The user's description of the bug

        Returns:
            BugReport instance or None if generation failed
        """
        pass


class Formatter(ABC):
    """Abstract interface for bug report formatters."""

    @abstractmethod
    def format(self, bug_report: BugReport) -> str:
        """
        Format a bug report for a specific platform.

        Args:
            bug_report: The bug report to format

        Returns:
            Formatted string ready for the target platform
        """
        pass
