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

    class Config:
        json_schema_extra = {
            "example": {
                "user_input": "there is no header displayed on the main page, i can see error 404 in js console"
            }
        }


class BugReportResponse(BaseModel):
    """Response model for bug report generation."""

    title: str
    description: str
    steps: str
    expected_result: str
    actual_result: str
    formatted_report: str

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Missing Header on Main Page with 404 Error",
                "description": "The main page header is not displaying, and there's a 404 error in the JavaScript console",
                "steps": "1. Navigate to the main page\n2. Open browser developer tools\n3. Check the console tab",
                "expected_result": "Header should be visible on the main page with no console errors",
                "actual_result": "Header is missing and 404 error appears in JS console",
                "formatted_report": "**Title:** Missing Header on Main Page...\n\n**Description:**..."
            }
        }
