# GitHub Action for Test Results to Plandek Timeseries API

This GitHub Action processes test results and sends them to Plandek's Timeseries API for tracking and analysis.

## Features

- Processes test results from JUnit XML format using `dorny/test-reporter`
- Extracts key metrics (total tests, passed, failed, skipped, success rate, duration)
- Creates timeseries in Plandek if they don't exist
- Includes repository and workflow context with each data point
- Handles authentication and error reporting

## Setup

1. Add the following secret to your GitHub repository:
   - `TIMESERIES_API_KEY`: Your API key for Plandek's Timeseries API

2. Configure the following variables (optional):
   - `TIMESERIES_API_URL`: Base URL for the timeseries API (defaults to `https://api.plandek.com/timeseries/v1`)

## Usage

1. Copy the workflow file to your repository:
   ```bash
   mkdir -p .github/workflows/
   cp timeseries-api/testing-data-github-actions/.github/workflows/process-test-results.yml .github/workflows/
   ```

2. Copy the script to your repository:
   ```bash
   mkdir -p .github/scripts/
   cp timeseries-api/testing-data-github-actions/.github/scripts/process_test_metrics.py .github/scripts/
   ```

3. The workflow will automatically run after your test workflow completes. Make sure to update the workflow trigger to match your test workflow name:

```yaml
on:
  workflow_run:
    workflows: ["Your Test Workflow Name"]
    types:
      - completed
```

## Example Workflow

Here's how the workflow is structured:

```yaml
name: Process Test Results

on:
  workflow_run:
    workflows: ["Run Tests"]  # Replace with your test workflow name
    types:
      - completed

jobs:
  process-test-results:
    name: Process Test Results
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests python-dotenv
    
    - name: Get test results
      id: test-results
      uses: dorny/test-reporter@v1
      with:
        name: Test Results
        path: test-results/**/*.xml  # Update this path to match your test results location
        reporter: java-junit
        fail-on-error: false
    
    - name: Process and send test metrics
      env:
        TIMESERIES_API_KEY: ${{ secrets.TIMESERIES_API_KEY }}
        TIMESERIES_API_URL: ${{ vars.TIMESERIES_API_URL || 'https://api.plandek.com/timeseries/v1' }}
      run: |
        python .github/scripts/process_test_metrics.py "${{ steps.test-results.outputs.data }}"

## Data Format

The following data is sent to the timeseries API:

```json
{
  "timestamp": "2023-01-01T12:00:00Z",
  "source": "github-actions",
  "repository": "owner/repo",
  "workflow": "CI",
  "run_id": "1234567890",
  "metrics": {
    "tests_total": 100,
    "tests_passed": 95,
    "tests_failed": 5,
    "tests_skipped": 0,
    "success_rate": 95.0,
    "duration_seconds": 120.5
  },
  "metadata": {
    "branch": "main",
    "commit_sha": "abc123def456",
    "run_attempt": "1"
  }
}
```

## Customization

You can customize the following:

1. **Test Results Path**: Update the `path` parameter in the workflow to match your test results location.
2. **Additional Metadata**: Modify the `process_test_metrics.py` script to include additional context or metrics.
3. **API Endpoint**: Override the default API endpoint using the `TIMESERIES_API_URL` variable.

## Requirements

- Python 3.8+
- `requests` and `python-dotenv` packages (installed automatically by the workflow)
