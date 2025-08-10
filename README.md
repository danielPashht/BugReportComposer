# Bug Reporter

A modular Python application for generating structured bug reports using Google's Generative AI API.

## Features

- **Modular Architecture**: Clean separation of concerns with SOLID principles
- **AI-Powered**: Uses Google Gemini API for intelligent bug report generation
- **Extensible**: Easy to add new formatters and LLM services
- **Docker Support**: Ready for containerization and deployment
- **Multiple Interfaces**: CLI ready, with architecture for API and web interfaces

## Architecture

The application follows a modular architecture with clear separation of concerns:

```
src/
├── core/           # Core models and interfaces
├── services/       # Business logic and external integrations
├── formatters/     # Output formatters for different platforms
├── prompts/        # LLM prompts separated from business logic
├── cli/           # Command line interface
└── config/        # Configuration management
```

### Key Components

- **Core Layer**: Contains data models, interfaces, and exceptions
- **Services Layer**: Business logic and LLM service implementations
- **Formatters Layer**: Platform-specific output formatting (Jira, etc.)
- **CLI Layer**: Command line interface implementation
- **Config Layer**: Environment-based configuration management

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables in `.env`:
   ```
   GEMINI_API_KEY=your_api_key_here
   GEMINI_MODEL=gemini-1.5-flash
   MAX_RETRIES=3
   ```

## Usage

### Command Line

```bash
# Using main.py
python main.py "App crashes when clicking save button"

# Using module syntax
python -m src "Login form doesn't validate email addresses"

# Using installed package (after pip install -e .)
bug-reporter "Navigation menu disappears on mobile devices"
```
### Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t bug-reporter .
docker run -e GEMINI_API_KEY=your_key bug-reporter "Bug description here"
```

## Development

Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

Run tests:
```bash
pytest
```

Code formatting:
```bash
black src/
isort src/
```

Type checking:
```bash
mypy src/
```

## Extending the Application

### Adding New Formatters

1. Create a new formatter class inheriting from `BaseFormatter`
2. Implement the `format` method
3. Register it in the formatters module

### Adding New LLM Services

1. Create a new service class implementing `LLMService` interface
2. Implement the `generate_bug_report` method
3. Register it in the services module

### Adding New Interfaces (API, Web)

The modular architecture makes it easy to add new interfaces:
- API: Create a new module under `src/api/`
- Web: Create a new module under `src/web/`
- Both can reuse the existing services and formatters

## License

MIT License

