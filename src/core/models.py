"""Data models for the Bug Reporter application."""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class BugReport:
    """Data model representing a structured bug report."""

    title: str
    description: str
    steps: str
    expected_result: str
    actual_result: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert the bug report to a dictionary."""
        return {
            "Title": self.title,
            "Description of the issue": self.description,
            "Steps": self.steps,
            "Expected result": self.expected_result,
            "Actual result": self.actual_result
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BugReport':
        """Create a BugReport instance from a dictionary."""
        return cls(
            title=data.get("Title", ""),
            description=data.get("Description of the issue", ""),
            steps=data.get("Steps", ""),
            expected_result=data.get("Expected result", ""),
            actual_result=data.get("Actual result", "")
        )

    def __str__(self) -> str:
        """Return a string representation of the bug report."""
        return f"BugReport(title='{self.title}', description='{self.description[:50]}...')"
