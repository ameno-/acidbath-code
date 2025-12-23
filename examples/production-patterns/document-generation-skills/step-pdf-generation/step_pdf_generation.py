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
