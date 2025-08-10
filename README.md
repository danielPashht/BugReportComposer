# Bug Reporter

A sophisticated bug reporting tool that transforms user descriptions into structured, professional bug reports using AI. Available as both a CLI tool and REST API.

## Features

- **AI-Powered Analysis**: Uses Google's Gemini AI to analyze user input and generate structured bug reports
- **Multiple Interfaces**: Available as both CLI and REST API
- **Structured Output**: Generates reports with title, description, steps, expected/actual results
- **JIRA Integration**: Formats reports for easy import into JIRA and other bug tracking systems
- **Validation**: Robust input validation and error handling

## Quick Start

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd bugReporter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export GOOGLE_API_KEY="your-gemini-api-key"
```

### CLI Usage

```bash
python main.py "there is no header displayed on the main page, i can see error 404 in js console"
```

### API Usage

1. Start the server:
```bash
python server.py
```

2. The API will be available at `http://localhost:8000`
3. Interactive documentation: `http://localhost:8000/docs`

## API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Endpoints

#### Generate Bug Report
**POST** `/bug-reports`

Generates a structured bug report from user input.

**Request Body:**
```json
{
  "user_input": "there is no header displayed on the main page, i can see error 404 in js console"
}
```

**Response:**
```json
{
  "title": "Missing Header on Main Page with 404 Error",
  "description": "The main page header is not displaying, and there's a 404 error in the JavaScript console",
  "steps": "1. Navigate to the main page\n2. Open browser developer tools\n3. Check the console tab",
  "expected_result": "Header should be visible on the main page with no console errors",
  "actual_result": "Header is missing and 404 error appears in JS console",
  "formatted_report": "**Title:** Missing Header on Main Page with 404 Error\n\n**Description:**\nThe main page header is not displaying, and there's a 404 error in the JavaScript console\n\n**Steps to reproduce:**\n1. Navigate to the main page\n2. Open browser developer tools\n3. Check the console tab\n\n**Expected result:**\nHeader should be visible on the main page with no console errors\n\n**Actual result:**\nHeader is missing and 404 error appears in JS console"
}
```

### Request Examples

#### Using curl
```bash
curl -X POST "http://localhost:8000/api/v1/bug-reports" \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "there is no header displayed on the main page, i can see error 404 in js console"
  }'
```

#### Using Python requests
```python
import requests

url = "http://localhost:8000/api/v1/bug-reports"
data = {
    "user_input": "there is no header displayed on the main page, i can see error 404 in js console"
}

response = requests.post(url, json=data)
print(response.json())
```

#### Using JavaScript fetch
```javascript
const response = await fetch('http://localhost:8000/api/v1/bug-reports', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    user_input: 'there is no header displayed on the main page, i can see error 404 in js console'
  })
});

const bugReport = await response.json();
console.log(bugReport);
```

### Error Responses

The API returns appropriate HTTP status codes and error messages:

**400 Bad Request** - Invalid input data
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "user_input"],
      "msg": "Field required"
    }
  ]
}
```

**500 Internal Server Error** - Processing failure
```json
{
  "detail": "Bug report generation failed: Unable to parse AI response"
}
```

## Project Structure

```
src/
├── api/           # FastAPI application
│   ├── app.py     # Application factory
│   ├── models.py  # Pydantic models
│   └── routes.py  # API endpoints
├── cli/           # Command-line interface
├── core/          # Core data models and interfaces
├── services/      # Business logic services
├── formatters/    # Output formatting
└── prompts/       # AI prompts
```

## Configuration

### Environment Variables

- `GOOGLE_API_KEY`: Required. Your Google Gemini API key
- `LOG_LEVEL`: Optional. Logging level (default: INFO)

### Development

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
pytest
```

3. Run with auto-reload:
```bash
python server.py
```

## Docker Support

### Build and run with Docker:
```bash
docker build -t bug-reporter .
docker run -p 8000:8000 -e GOOGLE_API_KEY="your-api-key" bug-reporter
```

### Using Docker Compose:
```bash
docker-compose up
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License