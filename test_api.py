#!/usr/bin/env python3
"""Test script for the FastAPI bug report endpoint."""

import requests
import json
import sys


def test_bug_report_api():
    """Test the bug report API endpoint."""
    url = "http://localhost:8000/api/v1/bug-reports"

    test_data = {
        "user_input": "there is no header displayed on the main page, i can see error 404 in js console"
    }

    try:
        print("Testing FastAPI bug report endpoint...")
        print(f"URL: {url}")
        print(f"Request data: {json.dumps(test_data, indent=2)}")
        print("-" * 50)

        response = requests.post(url, json=test_data, timeout=60)

        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")

        if response.status_code == 200:
            response_data = response.json()
            print("\nSUCCESS! Bug report generated:")
            print("-" * 50)
            print(f"Title: {response_data.get('title', 'N/A')}")
            print(f"Description: {response_data.get('description', 'N/A')}")
            print(f"Steps: {response_data.get('steps', 'N/A')}")
            print(f"Expected Result: {response_data.get('expected_result', 'N/A')}")
            print(f"Actual Result: {response_data.get('actual_result', 'N/A')}")
            print(f"\nFormatted Report:\n{response_data.get('formatted_report', 'N/A')}")
        else:
            print(f"\nERROR! Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the server. Make sure it's running on http://localhost:8000")
        return False
    except requests.exceptions.Timeout:
        print("ERROR: Request timed out")
        return False
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

    return response.status_code == 200


if __name__ == "__main__":
    success = test_bug_report_api()
    sys.exit(0 if success else 1)
