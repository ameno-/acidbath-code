#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "requests>=2.31.0",
#   "rich>=13.0.0",
# ]
# ///
"""
Search prediction markets by keyword.

Usage:
    uv run search.py --query "election" [--limit 10]

Arguments:
    --query, -q    Search term (required)
    --limit, -l    Max results (default: 10)
    --format, -f   Output format: json|table (default: table)
"""

import argparse
import json
import requests
from rich.console import Console
from rich.table import Table

KALSHI_API = "https://trading-api.kalshi.com/trade-api/v2"

def search_markets(query: str, limit: int = 10) -> list:
    """Search Kalshi markets by keyword."""
    response = requests.get(
        f"{KALSHI_API}/markets",
        params={"status": "open", "limit": limit},
        headers={"Accept": "application/json"}
    )
    response.raise_for_status()

    markets = response.json().get("markets", [])
    # Filter by query in title
    return [m for m in markets if query.lower() in m.get("title", "").lower()][:limit]

def main():
    parser = argparse.ArgumentParser(description="Search prediction markets")
    parser.add_argument("-q", "--query", required=True, help="Search term")
    parser.add_argument("-l", "--limit", type=int, default=10, help="Max results")
    parser.add_argument("-f", "--format", choices=["json", "table"], default="table")

    args = parser.parse_args()

    markets = search_markets(args.query, args.limit)

    if args.format == "json":
        print(json.dumps(markets, indent=2))
    else:
        console = Console()
        table = Table(title=f"Markets matching '{args.query}'")
        table.add_column("ID", style="cyan")
        table.add_column("Title", style="green")
        table.add_column("Volume", justify="right")

        for m in markets:
            table.add_row(
                m.get("ticker", ""),
                m.get("title", "")[:50],
                str(m.get("volume", 0))
            )

        console.print(table)

if __name__ == "__main__":
    main()
