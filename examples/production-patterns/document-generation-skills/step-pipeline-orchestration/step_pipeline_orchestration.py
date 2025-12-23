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
