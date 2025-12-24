#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "anthropic>=0.69.0",
#   "pandas>=2.0.0",
#   "python-dotenv>=1.0.0",
# ]
# ///
"""
Document generation pipeline using Claude Skills.

Usage:
    uv run document_pipeline.py --data sample_data.json --output ./reports

Generates Excel, PowerPoint, and PDF from structured data.
"""

import argparse
import json
import os
from pathlib import Path

import pandas as pd
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found in environment")

client = Anthropic(api_key=API_KEY)
MODEL = "claude-sonnet-4-5"

# Track token usage across pipeline
pipeline_tokens = {"input": 0, "output": 0}


def create_skills_message(prompt: str, skill_id: str, prefix: str = "") -> dict:
    """
    Create a document using Claude Skills API.

    Args:
        prompt: Document generation instructions
        skill_id: Which skill to use (xlsx, pptx, pdf)
        prefix: Filename prefix for output

    Returns:
        Dict with response and file info
    """
    response = client.beta.messages.create(
        model=MODEL,
        max_tokens=4096,
        container={"skills": [{"type": "anthropic", "skill_id": skill_id, "version": "latest"}]},
        tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
        messages=[{"role": "user", "content": prompt}],
        betas=[
            "code-execution-2025-08-25",
            "files-api-2025-04-14",
            "skills-2025-10-02",
        ],
    )

    # Track tokens
    pipeline_tokens["input"] += response.usage.input_tokens
    pipeline_tokens["output"] += response.usage.output_tokens

    return {
        "response": response,
        "tokens_in": response.usage.input_tokens,
        "tokens_out": response.usage.output_tokens,
    }


def generate_excel(data: dict, output_dir: Path) -> dict:
    """
    Generate Excel workbook with data, formulas, and charts.

    Best practice: 2-3 sheets per workbook for reliable generation.
    """
    summary = data.get("summary", {})
    metrics = summary.get("metrics", {})
    trends = summary.get("trends", [])

    prompt = f"""
Create an Excel workbook with 2 sheets:

Sheet 1 - "Summary":
- Title row: "{data.get('title', 'Report')}"
- Key metrics table:
  - Revenue: ${metrics.get('revenue', 0):,.2f}
  - Growth YoY: {metrics.get('revenue_growth_yoy', 0)}%
  - Net Income: ${metrics.get('net_income', 0):,.2f}
  - Operating Margin: {metrics.get('operating_margin', 0)}%
  - Customer Count: {metrics.get('customer_count', 0)}
  - Churn Rate: {metrics.get('churn_rate', 0)}%

Sheet 2 - "Trends":
- Data table with columns: Quarter, Revenue, Margin
- Data: {json.dumps(trends, indent=2)}
- Line chart showing Revenue over quarters
- Include SUM and AVERAGE formulas

Format professionally:
- Bold headers
- Currency format for dollar amounts
- Percentage format where appropriate
- Borders around data tables
"""

    result = create_skills_message(prompt, "xlsx", "financial_report_")
    print(f"  Excel: {result['tokens_in']:,} in, {result['tokens_out']:,} out")
    return result


def generate_powerpoint(data: dict, output_dir: Path) -> dict:
    """
    Generate executive presentation from data.

    Best practice: Clear, data-driven slides with minimal text.
    """
    summary = data.get("summary", {})

    prompt = f"""
Create a 4-slide executive presentation:

Slide 1 - Title:
- Title: "{data.get('title', 'Quarterly Report')}"
- Subtitle: "Executive Summary"
- Date: {data.get('date', 'Q4 2024')}

Slide 2 - Key Metrics:
- Title: "Performance Highlights"
- Two-column layout:
  Left: Key metrics with values
  Right: Bar chart of top metrics
- Data: {json.dumps(summary.get('metrics', {}), indent=2)}

Slide 3 - Trends:
- Title: "Quarterly Trends"
- Line chart showing progression
- Bullet points for insights
- Data: {json.dumps(summary.get('trends', []), indent=2)}

Slide 4 - Recommendations:
- Title: "Key Takeaways"
- 4-5 bullet points summarizing findings
- Clear call to action

Use professional corporate design:
- Dark blue (#003366) for headers
- Clean, modern layout
- Data-driven visualizations
"""

    result = create_skills_message(prompt, "pptx", "executive_summary_")
    print(f"  PowerPoint: {result['tokens_in']:,} in, {result['tokens_out']:,} out")
    return result


def generate_pdf(data: dict, output_dir: Path) -> dict:
    """
    Generate formal PDF documentation.

    Best practice: Clear sections, consistent formatting.
    """
    prompt = f"""
Create a PDF document:

DOCUMENT TITLE
{data.get('title', 'Report')}

EXECUTIVE SUMMARY
{data.get('executive_summary', 'Summary of key findings.')}

KEY METRICS
{json.dumps(data.get('summary', {}).get('metrics', {}), indent=2)}

ANALYSIS
- Document the methodology
- Present key findings
- Note any caveats or limitations

RECOMMENDATIONS
{json.dumps(data.get('recommendations', []), indent=2)}

APPENDIX
- Data sources
- Methodology notes
- Contact information

Format as a professional business document with:
- Clear section headers
- Consistent typography
- Page numbers
- Date stamp
"""

    result = create_skills_message(prompt, "pdf", "documentation_")
    print(f"  PDF: {result['tokens_in']:,} in, {result['tokens_out']:,} out")
    return result


def run_pipeline(data_path: str, output_dir: str) -> dict:
    """
    Run complete document generation pipeline.

    Returns:
        Dict with all results and token usage
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Load data
    with open(data_path) as f:
        data = json.load(f)

    print("=" * 60)
    print("DOCUMENT GENERATION PIPELINE")
    print("=" * 60)

    results = {}

    # Step 1: Excel
    print("\nStep 1/3: Generating Excel...")
    results["excel"] = generate_excel(data, output_path)

    # Step 2: PowerPoint
    print("\nStep 2/3: Generating PowerPoint...")
    results["powerpoint"] = generate_powerpoint(data, output_path)

    # Step 3: PDF
    print("\nStep 3/3: Generating PDF...")
    results["pdf"] = generate_pdf(data, output_path)

    # Summary
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)
    print(f"\nTotal Input Tokens:  {pipeline_tokens['input']:,}")
    print(f"Total Output Tokens: {pipeline_tokens['output']:,}")
    print(f"Total Tokens:        {pipeline_tokens['input'] + pipeline_tokens['output']:,}")

    # Cost estimate (Sonnet pricing: $3/M input, $15/M output)
    cost = (pipeline_tokens['input'] * 3 + pipeline_tokens['output'] * 15) / 1_000_000
    print(f"Estimated Cost:      ${cost:.4f}")

    return results


def main():
    parser = argparse.ArgumentParser(description="Generate documents from data")
    parser.add_argument("--data", required=True, help="Path to JSON data file")
    parser.add_argument("--output", default="./output", help="Output directory")
    args = parser.parse_args()

    run_pipeline(args.data, args.output)


if __name__ == "__main__":
    main()
