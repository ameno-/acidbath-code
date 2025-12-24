# Document Pipeline

## Source

**Blog Post:** [AI Document Skills: Automated File Generation That Actually Ships](https://blog.acidbath.com/blog/document-generation-skills)
**Date Extracted:** 2025-12-23

## Description

Complete document generation pipeline using Claude Skills API. Generates Excel workbooks, PowerPoint presentations, and PDF documents from structured JSON data.

This is a production-ready example that demonstrates:
- Claude Skills API integration for document generation
- Multi-format output (Excel, PowerPoint, PDF)
- Token usage tracking and cost estimation
- Pipeline orchestration pattern

## Quick Start

```bash
# Set your API key
export ANTHROPIC_API_KEY=your_key_here

# Run the pipeline with sample data
uv run document_pipeline.py --data sample_data.json --output ./reports
```

## Files

- **`document_pipeline.py`** - Complete pipeline implementation (215 lines)
- **`sample_data.json`** - Example input data for testing

## Dependencies

This script uses inline dependencies (PEP 723). Run with `uv run` to auto-install:

- anthropic>=0.69.0
- pandas>=2.0.0
- python-dotenv>=1.0.0

## Pipeline Steps

1. **Excel Generation** - Creates workbook with Summary and Trends sheets
2. **PowerPoint Generation** - Creates 4-slide executive presentation
3. **PDF Generation** - Creates formal documentation

## Token Usage

Typical pipeline run:
- Input tokens: ~6,300
- Output tokens: ~7,700
- Estimated cost: ~$0.13

## Blog Context

This code is from [AI Document Skills: Automated File Generation That Actually Ships](https://blog.acidbath.com/blog/document-generation-skills).

The blog post provides:
- Detailed explanation of Skills API usage
- Production deployment considerations
- Error handling and failure modes
- Best practices for document generation

## License

This code follows the **POC Rule**: working, copy-paste code you can use immediately.
See the [ACIDBATH blog](https://blog.acidbath.com) for more AI engineering content.
