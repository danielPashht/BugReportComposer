"""Custom exceptions for the Bug Reporter application."""


class BugReporterError(Exception):
    """Base exception for Bug Reporter application."""

    pass


class LLMServiceError(BugReporterError):
    """Exception raised when LLM service encounters an error."""

    pass


class ValidationError(BugReporterError):
    """Exception raised when validation fails."""

    pass


class BugReportServiceError:
    pass


class ConfigurationError(BugReporterError):
    """Exception raised when there's a configuration error."""

    pass
