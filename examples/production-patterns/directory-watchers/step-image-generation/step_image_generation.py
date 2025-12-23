#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "replicate>=0.25.0",
#   "requests>=2.31.0",
# ]
# ///
"""
Image Generation Agent

Reads prompts from a text file and generates images using Replicate.
Each line in the file is a separate prompt.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

import replicate
import requests


def generate_images(input_file: str, output_dir: str) -> list[str]:
    """Generate images from prompts in input file."""
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file) as f:
        prompts = [line.strip() for line in f if line.strip()]

    generated = []

    for i, prompt in enumerate(prompts):
        print(f"Generating {i+1}/{len(prompts)}: {prompt[:50]}...")

        output = replicate.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            input={
                "prompt": prompt,
                "width": 1024,
                "height": 1024,
            }
        )

        # Download the image
        if output:
            image_url = output[0]
            response = requests.get(image_url)

            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            safe_prompt = prompt[:30].replace(" ", "_").replace("/", "-")
            filename = f"{timestamp}-{i:03d}-{safe_prompt}.png"
            filepath = os.path.join(output_dir, filename)

            with open(filepath, "wb") as f:
                f.write(response.content)

            generated.append(filepath)
            print(f"  Saved: {filepath}")

    return generated


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: uv run image_gen.py <input_file> <output_dir>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    files = generate_images(input_file, output_dir)
    print(f"\nGenerated {len(files)} images")

    # Return output path
    print(output_dir)
