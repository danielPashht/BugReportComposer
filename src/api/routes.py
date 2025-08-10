"""API routes for bug report generation."""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from ..services.bug_report_service import BugReportService
from ..services.gemini_service import GeminiService
from ..formatters.jira_formatter import JiraFormatter
from ..core.exceptions import BugReporterError
from ..core.models import BugReport
from .models import BugReportRequest, BugReportResponse

router = APIRouter(prefix="/api/v1", tags=["bug-reports"])


def get_bug_report_service() -> BugReportService:
    """Dependency to create and return a bug report service instance."""
    llm_service = GeminiService()
    formatter = JiraFormatter()
    return BugReportService(llm_service, formatter)


@router.post("/bug-reports", response_model=BugReportResponse)
async def create_bug_report(
    request: BugReportRequest,
    service: BugReportService = Depends(get_bug_report_service)
) -> BugReportResponse:
    """
    Generate a formatted bug report from user input.

    Args:
        request: The bug report request containing user input
        service: The bug report service dependency

    Returns:
        A formatted bug report with structured fields

    Raises:
        HTTPException: If the bug report generation fails
    """
    try:
        # Generate the formatted report
        formatted_report = service.generate_formatted_report(request.user_input)

        if formatted_report is None:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate bug report"
            )

        # Also get the structured bug report for individual fields
        from ..prompts.bug_report_prompts import BugReportPrompts
        prompt = BugReportPrompts.create_bug_report_prompt(request.user_input)
        bug_report = service.llm_service.generate_bug_report(request.user_input)

        if bug_report is None:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate structured bug report"
            )

        return BugReportResponse(
            title=bug_report.title,
            description=bug_report.description,
            steps=bug_report.steps,
            expected_result=bug_report.expected_result,
            actual_result=bug_report.actual_result,
            formatted_report=formatted_report
        )

    except BugReporterError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Bug report generation failed: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
