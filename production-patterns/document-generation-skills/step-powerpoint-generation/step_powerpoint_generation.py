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
