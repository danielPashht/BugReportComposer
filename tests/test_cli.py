"""Tests for the CLI interface."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.cli.main import CLI, main
from src.core.exceptions import BugReporterError


class TestCLI:
    """Tests for CLI class."""

    @patch('src.cli.main.GeminiService')
    @patch('src.cli.main.JiraFormatter')
    @patch('src.cli.main.BugReportService')
    def test_cli_initialization(self, mock_bug_service, mock_formatter, mock_gemini):
        """Test that CLI can be initialized with its dependencies."""
        cli = CLI()

        assert cli is not None
        mock_gemini.assert_called_once()
        mock_formatter.assert_called_once()
        mock_bug_service.assert_called_once()

    def test_create_parser(self):
        """Test argument parser creation."""
        with patch('src.cli.main.GeminiService'), \
             patch('src.cli.main.JiraFormatter'), \
             patch('src.cli.main.BugReportService'):
            cli = CLI()
            parser = cli.create_parser()

            assert parser is not None
            # Test that it has the expected argument
            args = parser.parse_args(["test input"])
            assert args.input_text == "test input"

    def test_validate_input_success(self):
        """Test input validation with valid input."""
        with patch('src.cli.main.GeminiService'), \
             patch('src.cli.main.JiraFormatter'), \
             patch('src.cli.main.BugReportService'):
            cli = CLI()

            assert cli.validate_input("Valid bug description") is True
            assert cli.validate_input("   Valid with spaces   ") is True

    def test_validate_input_empty(self):
        """Test input validation with empty input."""
        with patch('src.cli.main.GeminiService'), \
             patch('src.cli.main.JiraFormatter'), \
             patch('src.cli.main.BugReportService'):
            cli = CLI()

            with patch('builtins.print') as mock_print:
                assert cli.validate_input("") is False
                assert cli.validate_input("   ") is False
                mock_print.assert_called_with("Error: Input text cannot be empty.")

    @patch('src.cli.main.GeminiService')
    @patch('src.cli.main.JiraFormatter')
    @patch('src.cli.main.BugReportService')
    def test_run_success(self, mock_bug_service_class, mock_formatter, mock_gemini):
        """Test successful CLI run."""
        mock_bug_service = Mock()
        mock_bug_service_class.return_value = mock_bug_service

        cli = CLI()

        with patch('sys.exit') as mock_exit:
            cli.run(["Test bug description"])

            mock_bug_service.process_bug_report.assert_called_once_with("Test bug description")
            mock_exit.assert_not_called()

    @patch('src.cli.main.GeminiService')
    @patch('src.cli.main.JiraFormatter')
    @patch('src.cli.main.BugReportService')
    def test_run_with_bug_reporter_error(self, mock_bug_service_class, mock_formatter, mock_gemini):
        """Test CLI run with BugReporterError."""
        mock_bug_service = Mock()
        mock_bug_service_class.return_value = mock_bug_service
        mock_bug_service.process_bug_report.side_effect = BugReporterError("Test error")

        cli = CLI()

        with patch('builtins.print') as mock_print, \
             patch('sys.exit') as mock_exit:
            cli.run(["Test bug description"])

            mock_print.assert_called_with("Error: Test error")
            mock_exit.assert_called_with(1)

    @patch('src.cli.main.GeminiService')
    @patch('src.cli.main.JiraFormatter')
    @patch('src.cli.main.BugReportService')
    def test_run_with_unexpected_error(self, mock_bug_service_class, mock_formatter, mock_gemini):
        """Test CLI run with unexpected error."""
        mock_bug_service = Mock()
        mock_bug_service_class.return_value = mock_bug_service
        mock_bug_service.process_bug_report.side_effect = Exception("Unexpected error")

        cli = CLI()

        with patch('builtins.print') as mock_print, \
             patch('sys.exit') as mock_exit:
            cli.run(["Test bug description"])

            mock_print.assert_called_with("Unexpected error: Unexpected error")
            mock_exit.assert_called_with(1)

    @patch('src.cli.main.GeminiService')
    @patch('src.cli.main.JiraFormatter')
    @patch('src.cli.main.BugReportService')
    def test_run_with_empty_input(self, mock_bug_service_class, mock_formatter, mock_gemini):
        """Test CLI run with empty input."""
        cli = CLI()

        with patch('builtins.print') as mock_print, \
             patch('sys.exit') as mock_exit:
            cli.run([""])

            mock_print.assert_called_with("Error: Input text cannot be empty.")
            mock_exit.assert_called_with(1)


class TestCLIMain:
    """Tests for CLI main function."""

    @patch('src.cli.main.CLI')
    def test_main_function(self, mock_cli_class):
        """Test main function creates CLI and runs it."""
        mock_cli = Mock()
        mock_cli_class.return_value = mock_cli

        main()

        mock_cli_class.assert_called_once()
        mock_cli.run.assert_called_once()
