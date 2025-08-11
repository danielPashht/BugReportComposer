"""Pydantic schemas for bug report validation."""

from pydantic import BaseModel, Field


class BugReportSchema(BaseModel):
    """Schema for validating bug report JSON from LLM."""

    title: str = Field(alias="Title", description="Bug report title")
    description_of_the_issue: str = Field(
        alias="Description", description="Description of the bug"
    )
    steps: str = Field(alias="Steps", description="Steps to reproduce")
    expected_result: str = Field(
        alias="Expected result", description="Expected behavior"
    )
    actual_result: str = Field(alias="Actual result", description="Actual behavior")

    class Config:
        validate_by_name = True
