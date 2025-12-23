#!/usr/bin/env python3
"""
Local validation script for all code examples in acidbath-code repository.

This script validates:
- Python files (syntax check)
- Bash scripts (shellcheck if available)
- JSON/YAML files (schema validation)
- Repository structure (READMEs, manifest)
"""

import sys
import json
import subprocess
from pathlib import Path
from typing import List, Tuple
import yaml


def validate_python_files(repo_root: Path) -> List[Tuple[Path, bool, str]]:
    """Validate all Python files."""
    results = []
    python_files = list(repo_root.glob('examples/**/*.py'))

    print(f"Validating {len(python_files)} Python files...")

    for py_file in python_files:
        try:
            subprocess.run(
                ['python', '-m', 'py_compile', str(py_file)],
                check=True,
                capture_output=True,
                timeout=10
            )
            results.append((py_file, True, "Valid"))
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode('utf-8') if e.stderr else "Syntax error"
            results.append((py_file, False, error_msg))
        except Exception as e:
            results.append((py_file, False, str(e)))

    return results


def validate_bash_files(repo_root: Path) -> List[Tuple[Path, bool, str]]:
    """Validate all bash scripts."""
    results = []
    bash_files = list(repo_root.glob('examples/**/*.sh'))

    # Check if shellcheck is available
    try:
        subprocess.run(['shellcheck', '--version'], capture_output=True, check=True)
        has_shellcheck = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        has_shellcheck = False
        print("⚠️  shellcheck not available, skipping bash validation")

    if not has_shellcheck:
        return results

    print(f"Validating {len(bash_files)} bash scripts...")

    for bash_file in bash_files:
        try:
            result = subprocess.run(
                ['shellcheck', str(bash_file)],
                capture_output=True,
                timeout=10
            )
            if result.returncode == 0:
                results.append((bash_file, True, "Valid"))
            else:
                results.append((bash_file, False, result.stdout.decode('utf-8')))
        except Exception as e:
            results.append((bash_file, False, str(e)))

    return results


def validate_json_yaml_files(repo_root: Path) -> List[Tuple[Path, bool, str]]:
    """Validate all JSON and YAML files."""
    results = []

    # JSON files
    json_files = list(repo_root.glob('examples/**/*.json'))
    print(f"Validating {len(json_files)} JSON files...")

    for json_file in json_files:
        try:
            with open(json_file) as f:
                json.load(f)
            results.append((json_file, True, "Valid"))
        except json.JSONDecodeError as e:
            results.append((json_file, False, f"Invalid JSON: {e}"))
        except Exception as e:
            results.append((json_file, False, str(e)))

    # YAML files
    yaml_files = list(repo_root.glob('examples/**/*.yaml')) + list(repo_root.glob('examples/**/*.yml'))
    print(f"Validating {len(yaml_files)} YAML files...")

    for yaml_file in yaml_files:
        try:
            with open(yaml_file) as f:
                yaml.safe_load(f)
            results.append((yaml_file, True, "Valid"))
        except yaml.YAMLError as e:
            results.append((yaml_file, False, f"Invalid YAML: {e}"))
        except Exception as e:
            results.append((yaml_file, False, str(e)))

    return results


def validate_structure(repo_root: Path) -> List[Tuple[str, bool, str]]:
    """Validate repository structure."""
    results = []

    # Check that all example directories have READMEs
    example_dirs = [
        d for d in (repo_root / 'examples').rglob('*')
        if d.is_dir() and len(d.parts) >= len((repo_root / 'examples').parts) + 3
    ]

    print(f"Checking {len(example_dirs)} example directories for READMEs...")

    for example_dir in example_dirs:
        readme_path = example_dir / 'README.md'
        if readme_path.exists():
            results.append((str(example_dir), True, "README exists"))
        else:
            results.append((str(example_dir), False, "Missing README.md"))

    # Check manifest if it exists
    manifest_path = repo_root / 'manifest.json'
    if manifest_path.exists():
        try:
            with open(manifest_path) as f:
                json.load(f)
            results.append(("manifest.json", True, "Valid"))
        except json.JSONDecodeError as e:
            results.append(("manifest.json", False, f"Invalid JSON: {e}"))

    return results


def print_results(category: str, results: List[Tuple]):
    """Print validation results."""
    print(f"\n{'='*60}")
    print(f"{category}")
    print('='*60)

    valid_count = sum(1 for _, valid, _ in results if valid)
    total_count = len(results)

    for item, valid, message in results:
        status = "✅" if valid else "❌"
        print(f"{status} {item}")
        if not valid:
            print(f"   {message}")

    print(f"\nResult: {valid_count}/{total_count} passed")

    return valid_count == total_count


def main():
    """Main execution."""
    repo_root = Path(__file__).parent.parent

    print("ACIDBATH Code Repository Validation")
    print("=" * 60)

    all_passed = True

    # Python validation
    python_results = validate_python_files(repo_root)
    if python_results:
        all_passed &= print_results("Python Files", python_results)

    # Bash validation
    bash_results = validate_bash_files(repo_root)
    if bash_results:
        all_passed &= print_results("Bash Scripts", bash_results)

    # JSON/YAML validation
    json_yaml_results = validate_json_yaml_files(repo_root)
    if json_yaml_results:
        all_passed &= print_results("JSON/YAML Files", json_yaml_results)

    # Structure validation
    structure_results = validate_structure(repo_root)
    if structure_results:
        all_passed &= print_results("Repository Structure", structure_results)

    # Final summary
    print(f"\n{'='*60}")
    if all_passed:
        print("✅ All validation checks passed!")
        sys.exit(0)
    else:
        print("❌ Some validation checks failed")
        sys.exit(1)


if __name__ == '__main__':
    main()
