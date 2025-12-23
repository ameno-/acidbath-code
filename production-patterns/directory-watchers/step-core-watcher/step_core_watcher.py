#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "watchdog>=4.0.0",
#   "pyyaml>=6.0",
#   "rich>=13.0.0",
#   "anthropic>=0.40.0",
# ]
# ///
"""
Drop Zone Watcher - File-based AI automation

Usage:
    uv run drop_watcher.py [--config drops.yaml]

Watches configured directories and triggers agents on file events.
"""

import argparse
import fnmatch
import os
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path

import yaml
from anthropic import Anthropic
from rich.console import Console
from rich.panel import Panel
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

console = Console()

class DropZoneHandler(FileSystemEventHandler):
    def __init__(self, zone_name: str, zone_config: dict, global_config: dict):
        self.zone_name = zone_name
        self.zone_config = zone_config
        self.global_config = global_config
        self.patterns = zone_config.get("patterns", ["*"])
        self.agent_name = zone_config.get("agent")
        self.agent_config = global_config["agents"].get(self.agent_name, {})

    def on_created(self, event):
        if event.is_directory:
            return
        if "created" not in self.zone_config.get("events", ["created"]):
            return
        self._process_file(event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        if "modified" not in self.zone_config.get("events", []):
            return
        self._process_file(event.src_path)

    def _matches_pattern(self, filepath: str) -> bool:
        filename = os.path.basename(filepath)
        return any(fnmatch.fnmatch(filename, p) for p in self.patterns)

    def _process_file(self, filepath: str):
        if not self._matches_pattern(filepath):
            return

        # Wait for file to be fully written
        time.sleep(0.5)

        console.print(Panel(
            f"[bold green]Processing:[/] {filepath}\n"
            f"[bold blue]Zone:[/] {self.zone_name}\n"
            f"[bold yellow]Agent:[/] {self.agent_name}",
            title="Drop Detected"
        ))

        try:
            output_path = self._run_agent(filepath)
            self._archive_file(filepath)
            console.print(f"[green]✓[/] Output: {output_path}")
        except Exception as e:
            console.print(f"[red]✗[/] Error: {e}")

    def _run_agent(self, filepath: str) -> str:
        agent_type = self.agent_config.get("type", "bash")
        output_dir = self._get_output_dir()

        if agent_type == "bash":
            return self._run_bash_agent(filepath, output_dir)
        elif agent_type == "claude":
            return self._run_claude_agent(filepath, output_dir)
        elif agent_type == "python":
            return self._run_python_agent(filepath, output_dir)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")

    def _run_bash_agent(self, filepath: str, output_dir: str) -> str:
        command = self.agent_config["command"].format(
            file=filepath,
            output_dir=output_dir
        )
        subprocess.run(command, shell=True, check=True)
        return output_dir

    def _run_claude_agent(self, filepath: str, output_dir: str) -> str:
        prompt_file = self.agent_config.get("prompt_file")
        model = self.agent_config.get("model", "claude-3-5-sonnet-20241022")

        # Load prompt template
        with open(prompt_file) as f:
            prompt_template = f.read()

        # Read input file
        with open(filepath) as f:
            content = f.read()

        # Substitute variables
        prompt = prompt_template.replace("{content}", content)
        prompt = prompt.replace("{filename}", os.path.basename(filepath))

        # Call Claude
        client = Anthropic()
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.content[0].text

        # Write output
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_filename = f"{timestamp}-{Path(filepath).stem}.md"
        output_path = os.path.join(output_dir, output_filename)

        os.makedirs(output_dir, exist_ok=True)
        with open(output_path, "w") as f:
            f.write(result)

        return output_path

    def _run_python_agent(self, filepath: str, output_dir: str) -> str:
        script = self.agent_config["script"]
        result = subprocess.run(
            ["uv", "run", script, filepath, output_dir],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()

    def _get_output_dir(self) -> str:
        base = os.path.expanduser(self.global_config.get("output_dir", "~/output"))
        return os.path.join(base, self.zone_name)

    def _archive_file(self, filepath: str):
        archive_base = os.path.expanduser(
            self.global_config.get("archive_dir", "~/archive")
        )
        archive_dir = os.path.join(archive_base, self.zone_name)
        os.makedirs(archive_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = os.path.basename(filepath)
        archive_path = os.path.join(archive_dir, f"{timestamp}-{filename}")

        shutil.move(filepath, archive_path)


def load_config(config_path: str) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def setup_watchers(config: dict) -> Observer:
    observer = Observer()

    for zone_name, zone_config in config.get("zones", {}).items():
        directory = os.path.expanduser(zone_config["directory"])
        os.makedirs(directory, exist_ok=True)

        handler = DropZoneHandler(zone_name, zone_config, config)
        observer.schedule(handler, directory, recursive=False)

        console.print(f"[blue]Watching:[/] {directory} → {zone_config['agent']}")

    return observer


def main():
    parser = argparse.ArgumentParser(description="Drop Zone Watcher")
    parser.add_argument("--config", default="drops.yaml", help="Config file path")
    args = parser.parse_args()

    config = load_config(args.config)

    console.print(Panel(
        "[bold]Drop Zone Watcher[/]\n"
        "Drag files into watched directories to trigger AI agents.",
        title="Starting"
    ))

    observer = setup_watchers(config)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        console.print("[yellow]Shutting down...[/]")

    observer.join()


if __name__ == "__main__":
    main()
