#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "anthropic>=0.40.0",
# ]
# ///
"""
Calculator agent with custom tool - demonstrates tool integration.

Usage:
    uv run calculator_agent.py "what is 15% of 847?"
"""

import json
import sys
from anthropic import Anthropic

SYSTEM_PROMPT = """
You are a calculator agent.
You have access to a calculate tool for mathematical operations.
Always use the calculate tool for any math - never do mental math.
After getting the result, explain it clearly to the user.
"""

TOOLS = [
    {
        "name": "calculate",
        "description": "Evaluate a mathematical expression. Supports +, -, *, /, **, (), and common functions like sqrt, sin, cos, log.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to evaluate, e.g., '(15/100) * 847' or 'sqrt(144)'"
                }
            },
            "required": ["expression"]
        }
    }
]


def execute_calculate(expression: str) -> str:
    """Execute a math expression safely."""
    import math
    # Safe eval with only math functions
    allowed = {
        'sqrt': math.sqrt,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'log': math.log,
        'log10': math.log10,
        'exp': math.exp,
        'pi': math.pi,
        'e': math.e,
        'abs': abs,
        'round': round,
    }
    try:
        result = eval(expression, {"__builtins__": {}}, allowed)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def run_agent(user_message: str) -> str:
    client = Anthropic()

    messages = [{"role": "user", "content": user_message}]

    # First API call
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        tools=TOOLS,
        messages=messages
    )

    # Handle tool use
    while response.stop_reason == "tool_use":
        # Find the tool use block
        tool_use = next(
            block for block in response.content
            if block.type == "tool_use"
        )

        # Execute the tool
        if tool_use.name == "calculate":
            result = execute_calculate(tool_use.input["expression"])
        else:
            result = f"Unknown tool: {tool_use.name}"

        # Add assistant message and tool result
        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": [{
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": result
            }]
        })

        # Continue the conversation
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages
        )

    # Return final text response
    return next(
        block.text for block in response.content
        if hasattr(block, "text")
    )


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run calculator_agent.py <question>")
        sys.exit(1)

    result = run_agent(" ".join(sys.argv[1:]))
    print(result)


if __name__ == "__main__":
    main()
