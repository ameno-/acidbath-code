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
