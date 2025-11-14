# aws-bedrock-cost-tool

[![CI](https://github.com/dnvriend/aws-bedrock-cost-tool/actions/workflows/ci.yml/badge.svg)](https://github.com/dnvriend/aws-bedrock-cost-tool/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://github.com/python/mypy)
[![AI Generated](https://img.shields.io/badge/AI-Generated-blueviolet.svg)](https://www.anthropic.com/claude)
[![Built with Claude Code](https://img.shields.io/badge/Built_with-Claude_Code-5A67D8.svg)](https://www.anthropic.com/claude/code)

A professional CLI tool for analyzing AWS Bedrock model costs with comprehensive reporting and visualization capabilities.

## Table of Contents

- [About](#about)
  - [What is AWS Bedrock?](#what-is-aws-bedrock)
  - [Why This CLI Tool?](#why-this-cli-tool)
- [Use Cases](#use-cases)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Basic Examples](#basic-examples)
  - [Output Formats](#output-formats)
  - [Detail Levels](#detail-levels)
  - [Advanced Usage](#advanced-usage)
- [Library Usage](#library-usage)
- [Development](#development)
- [Resources](#resources)
- [License](#license)

## About

### What is AWS Bedrock?

[AWS Bedrock](https://aws.amazon.com/bedrock/) is Amazon's fully managed service providing access to foundation models from leading AI companies including Anthropic (Claude), Meta (Llama), Amazon (Titan and Nova), Cohere, AI21 Labs, and Stability AI.

### Why This CLI Tool?

**aws-bedrock-cost-tool** provides CLI-first cost analysis for AWS Bedrock with an agent-friendly design that enables:

- 🤖 **Agent Integration**: Structured commands and JSON output enable AI agents (Claude Code, MCP servers) to reason and act effectively in ReAct loops
- 🔧 **Composable Architecture**: JSON to stdout, logs to stderr for easy piping and integration with automation tools
- 📦 **Reusable Building Blocks**: Commands serve as building blocks for skills, automation pipelines, and custom workflows
- ✅ **Reliability**: Type-safe implementation with comprehensive testing ensures predictable behavior in automated systems
- 📊 **Dual-Mode Operation**: Works both as a CLI tool and as an importable Python library

## Use Cases

- 💰 **Cost Monitoring**: Track daily Bedrock spending across all models and regions
- 📈 **Usage Analysis**: Analyze token consumption patterns (input/output/cache) by model
- 🔍 **Budget Tracking**: Monitor costs against budgets with quick summaries
- 🤖 **Automation**: Integrate into CI/CD pipelines, cost alerting systems, or reporting workflows
- 📊 **Trend Analysis**: Visualize cost trends over time with ASCII plots
- 🎯 **Model Comparison**: Compare costs across different Bedrock models and regions

## Features

- ✨ **Flexible Time Periods**: Support for days (7d), weeks (2w), months (1m) up to 365 days
- 📊 **Multiple Output Formats**:
  - JSON (default, machine-readable)
  - ASCII tables (termtables)
  - Time series plots (termplotlib)
  - Bar charts by model
  - Quick summaries
- 🎚️ **Three Detail Levels**:
  - **Basic**: Model totals only
  - **Standard**: Model totals + usage type breakdown (input/output/cache tokens)
  - **Full**: Complete breakdown including regional costs
- 🔐 **AWS Profile Support**: Override credentials with `--profile` flag
- ⚡ **Fast & Efficient**: Direct Cost Explorer API integration
- 🎯 **Agent-Friendly**: Clear error messages, structured output, composable design
- 📦 **Dual-Mode**: Use as CLI or import as Python library
- 🧪 **Fully Tested**: Comprehensive test suite with type safety

## Installation

### Prerequisites

- Python 3.14 or higher
- AWS CLI configured with credentials
- [uv](https://github.com/astral-sh/uv) package manager
- AWS account with Cost Explorer enabled
- IAM permissions: `ce:GetCostAndUsage`

### Install Globally with uv

```bash
# Clone repository
git clone https://github.com/dnvriend/aws-bedrock-cost-tool.git
cd aws-bedrock-cost-tool

# Install dependencies
uv sync

# Build and install globally
uv build
uv tool install dist/aws_bedrock_cost_tool-0.1.0-py3-none-any.whl

# Verify installation
aws-bedrock-cost-tool --version
```

### Install with mise (Development)

```bash
cd aws-bedrock-cost-tool
mise trust
mise install
uv sync
make pipeline
```

## Configuration

### AWS Credentials

The tool requires AWS credentials configured via one of:

1. **AWS CLI Profile**:
   ```bash
   aws configure --profile my-profile
   aws-bedrock-cost-tool --profile my-profile
   ```

2. **Environment Variables**:
   ```bash
   export AWS_PROFILE=my-profile
   export AWS_ACCESS_KEY_ID=your-access-key
   export AWS_SECRET_ACCESS_KEY=your-secret-key
   export AWS_REGION=us-east-1  # Cost Explorer is global but credentials need region
   ```

3. **IAM Role** (EC2/ECS/Lambda): Automatically detected

### Required IAM Permissions

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ce:GetCostAndUsage",
      "Resource": "*"
    }
  ]
}
```

### Cost Explorer Setup

Cost Explorer must be enabled in your AWS account:
- Navigate to **AWS Cost Explorer** in AWS Console
- Click **Enable Cost Explorer** if not already enabled
- Data becomes available within 24 hours

## Usage

### Basic Examples

```bash
# Default: JSON output for last 30 days
aws-bedrock-cost-tool

# Quick summary (total + top 3 models)
aws-bedrock-cost-tool --summary-only

# Human-readable table
aws-bedrock-cost-tool --table

# Last 7 days with specific profile
aws-bedrock-cost-tool --period 7d --profile production

# Last 2 weeks
aws-bedrock-cost-tool --period 2w

# Last 3 months
aws-bedrock-cost-tool --period 3m

# Verbose logging (show API calls)
aws-bedrock-cost-tool --verbose
```

### Output Formats

**JSON Output** (default, piping-friendly):
```bash
aws-bedrock-cost-tool | jq '.total_cost'
aws-bedrock-cost-tool | jq '.models[0].model_name'
aws-bedrock-cost-tool | jq '.models[] | select(.model_name | contains("Sonnet"))'
```

**Table Output**:
```bash
aws-bedrock-cost-tool --table
```

**Time Series Plot**:
```bash
aws-bedrock-cost-tool --plot-time
```

**Bar Chart** (model costs):
```bash
aws-bedrock-cost-tool --plot-models
```

**All Visualizations**:
```bash
aws-bedrock-cost-tool --all-visual
```

**Quick Summary**:
```bash
aws-bedrock-cost-tool --summary-only
# Output: Total: $42.50 | Top: Claude Sonnet 4.5 ($35.20), Claude Haiku 4.5 ($5.30), Llama 3.1 70B ($2.00)
```

### Detail Levels

**Basic** (model totals only):
```bash
aws-bedrock-cost-tool --detail basic --table
```

**Standard** (default, includes usage type breakdown):
```bash
aws-bedrock-cost-tool --detail standard --table
```

**Full** (includes regional breakdown):
```bash
aws-bedrock-cost-tool --detail full --table
```

### Advanced Usage

**Combine Options**:
```bash
# 90 days, full detail, all visualizations
aws-bedrock-cost-tool --period 90d --detail full --all-visual

# Last month with specific profile and verbose logging
aws-bedrock-cost-tool --period 1m --profile prod --verbose --table

# Quick cost check
aws-bedrock-cost-tool --period 7d --summary-only
```

**Automation Examples**:
```bash
# Daily cost monitoring script
#!/bin/bash
COST=$(aws-bedrock-cost-tool --period 7d | jq -r '.total_cost')
if (( $(echo "$COST > 100" | bc -l) )); then
  echo "Warning: Weekly Bedrock costs exceed $100: \$${COST}"
fi

# Export to CSV for reporting
aws-bedrock-cost-tool --period 30d | jq -r '.models[] | [.model_name, .total_cost] | @csv' > costs.csv

# Get top model
TOP_MODEL=$(aws-bedrock-cost-tool | jq -r '.models[0].model_name')
echo "Highest cost model: $TOP_MODEL"
```

## Library Usage

Use `aws-bedrock-cost-tool` as a Python library:

```python
from aws_bedrock_cost_tool import (
    create_cost_explorer_client,
    query_bedrock_costs,
    analyze_cost_data,
    parse_period,
    calculate_date_range,
    format_date_for_aws,
)

# Parse period and calculate dates
days = parse_period("30d")
start_date, end_date = calculate_date_range(days)

# Create client and query
client = create_cost_explorer_client(profile_name="my-profile")
response = query_bedrock_costs(
    client,
    format_date_for_aws(start_date),
    format_date_for_aws(end_date)
)

# Analyze data
cost_data = analyze_cost_data(response, start_date, end_date, detail="standard")

# Access results
print(f"Total cost: ${cost_data['total_cost']:.2f}")
for model in cost_data['models']:
    print(f"{model['model_name']}: ${model['total_cost']:.2f}")
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/dnvriend/aws-bedrock-cost-tool.git
cd aws-bedrock-cost-tool

# Install dependencies
make install

# Show available commands
make help
```

### Available Make Commands

```bash
make install          # Install dependencies
make format           # Format code with ruff
make lint             # Run linting with ruff
make typecheck        # Run type checking with mypy
make test             # Run tests with pytest
make check            # Run all checks (lint + typecheck + test)
make pipeline         # Run full pipeline (format, lint, typecheck, test, build, install-global)
make build            # Build package
make install-global   # Install globally with uv tool
make run ARGS="..."   # Run aws-bedrock-cost-tool locally
make clean            # Remove build artifacts
```

### Project Structure

```
aws_bedrock_cost_tool/
├── __init__.py              # Public API exports
├── cli.py                   # CLI entry point
├── utils.py                 # Period parsing, date utilities
├── core/                    # Core library functions
│   ├── models.py           # TypedDict data models
│   ├── cost_explorer.py    # boto3 Cost Explorer client
│   └── analyzer.py         # Cost aggregation logic
└── reporting/               # Reporting and visualization
    ├── json_formatter.py   # JSON output
    ├── summary.py          # Quick summaries
    ├── table_renderer.py   # termtables rendering
    └── plots.py            # termplotlib charts
```

### Running Tests

```bash
# Run all tests
make test

# Run with verbose output
uv run pytest tests/ -v

# Run specific test
uv run pytest tests/test_utils.py -v

# Run with coverage
uv run pytest tests/ --cov=aws_bedrock_cost_tool --cov-report=html
```

## Resources

- **AWS Bedrock**: https://aws.amazon.com/bedrock/
- **AWS Cost Explorer API**: https://docs.aws.amazon.com/cost-management/latest/userguide/ce-api.html
- **Boto3 Documentation**: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
- **termplotlib**: https://github.com/nschloe/termplotlib
- **termtables**: https://github.com/nschloe/termtables

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Dennis Vriend**

- GitHub: [@dnvriend](https://github.com/dnvriend)
- Email: dvriend@ilionx.com

## Acknowledgments

- Built with [Click](https://click.palletsprojects.com/) for CLI framework
- Developed with [uv](https://github.com/astral-sh/uv) for fast Python tooling
- Visualizations powered by [termplotlib](https://github.com/nschloe/termplotlib) and [termtables](https://github.com/nschloe/termtables)
- AWS integration via [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

---

**Generated with AI**

This project was developed using [Claude Code](https://www.anthropic.com/claude/code), an AI-powered development tool by [Anthropic](https://www.anthropic.com/). The implementation follows professional CLI-first design principles optimized for both human users and AI agent integration.

Made with ❤️ using Python 3.14
