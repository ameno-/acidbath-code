#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "anthropic>=0.40.0",
# ]
# ///
"""
Simplest possible custom agent - demonstrates system prompt override.

Usage:
    uv run pong_agent.py "any message"
"""

import sys
from anthropic import Anthropic

SYSTEM_PROMPT = """
You are a pong agent.
Always respond exactly with "pong".
Nothing else. No explanations. Just "pong".
"""

def main():
    if len(sys.argv) < 2:
        print("Usage: uv run pong_agent.py <message>")
        sys.exit(1)

    client = Anthropic()

    response = client.messages.create(
        model="claude-3-haiku-20240307",  # Cheapest model for simple task
        max_tokens=10,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": sys.argv[1]}]
    )

    print(response.content[0].text)


if __name__ == "__main__":
    main()
