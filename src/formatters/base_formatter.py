"""Base formatter interface and common functionality."""

from abc import ABC, abstractmethod
from ..core.interfaces import Formatter
from ..core.models import BugReport


class BaseFormatter(Formatter, ABC):
    """Base formatter with common functionality."""

    def __init__(self):
        """Initialize the base formatter."""
        pass

    @abstractmethod
    def format(self, bug_report: BugReport) -> str:
        """Format a bug report for a specific platform."""
        pass

    def _format_field(self, label: str, value: str, **kwargs) -> str:
        """
        Format a single field. Can be overridden by subclasses.

        Args:
            label: Field label
            value: Field value
            **kwargs: Additional formatting options

        Returns:
            Formatted field string
        """
        return f"{label}:\n{value}"
