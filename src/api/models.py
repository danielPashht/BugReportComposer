"""API models for the Bug Reporter application."""

from pydantic import BaseModel, Field


class BugReportRequest(BaseModel):
    """Request model for bug report generation."""

    user_input: str = Field(
        ...,
        description="User's description of the bug",
        min_length=1,
        max_length=5000
    )


class BugReportResponse(BaseModel):
    """Response model for bug report generation."""

    title: str
    description: str
    steps: str
    expected_result: str
    actual_result: str
    formatted_report: str
