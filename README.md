# ACIDBATH Code Repository

This repository contains complete, working code examples extracted from the [ACIDBATH blog](https://acidbath.sh). All code follows the **POC Rule**: it's working, copy-paste code that you can use immediately.

## Purpose

ACIDBATH blog posts often include substantial code examples that demonstrate production-ready patterns, agentic workflows, and developer tools. To improve blog readability while maintaining code accessibility, complete examples are hosted here with full context and usage instructions.

## Organization

Code is organized by category and source blog post:

```
examples/
├── agentic-patterns/        # AI agent patterns and architectures
├── production-patterns/     # Production-ready code patterns
├── workflow-tools/          # Automation scripts and utilities
└── configurations/          # Config files and templates
```

Each example includes:
- **Source code** - Complete, runnable implementation
- **README.md** - Context, usage instructions, and modifications guide
- **Blog post link** - Reference to original post for detailed explanation

## Categories

### Agentic Patterns

Code examples demonstrating AI agent patterns, workflows, and architectures.

**Topics:**
- Multi-agent orchestration
- Agent communication protocols
- Prompt engineering patterns
- Context management
- Agent coordination systems

**Source Posts:**
- [Building Multi-Agent Architectures](https://acidbath.sh/blog/agent-architecture)
- [Claude Skills Deep Dive](https://acidbath.sh/blog/claude-skills-deep-dive)
- [Context Engineering](https://acidbath.sh/blog/context-engineering)

### Production Patterns

Production-ready code for real-world applications.

**Topics:**
- Error handling and resilience
- Monitoring and observability
- File system operations
- Document generation
- Performance optimization

**Source Posts:**
- [Directory Watchers and File System Monitoring](https://acidbath.sh/blog/directory-watchers)
- [Document Generation Skills](https://acidbath.sh/blog/document-generation-skills)

### Workflow Tools

Utility scripts, automation tools, and workflow helpers.

**Topics:**
- CLI tools
- Automation scripts
- File processing utilities
- Data transformation
- Build and deployment tools

**Source Posts:**
- [Single-File Scripts for Maximum Impact](https://acidbath.sh/blog/single-file-scripts)
- [Workflow Prompts and Templates](https://acidbath.sh/blog/workflow-prompts)

### Configurations

Configuration files, schemas, and templates.

**Topics:**
- CI/CD configurations
- JSON schemas
- YAML templates
- Environment setups
- Container configs

## Usage

### Browse Examples

Navigate to any category directory to see available examples:

```bash
cd examples/agentic-patterns/agent-architecture/
ls -la
```

Each example directory contains:
- Source code files
- README.md with usage instructions
- Any necessary configuration files

### Run an Example

1. Navigate to the example directory
2. Read the README.md for prerequisites
3. Follow the installation and usage instructions

```bash
cd examples/production-patterns/directory-watchers/file-system-watcher/
cat README.md
python watcher.py
```

### Adapt for Your Project

All code is designed to be copy-paste ready with minimal modifications:

1. Read the example README for context
2. Copy the code to your project
3. Modify as needed for your use case
4. See the original blog post for detailed explanation

## Validation

All code in this repository is validated:

- **Python**: Syntax checked with `ast.parse()`
- **Bash**: Validated with `shellcheck` (where available)
- **JSON/YAML**: Schema validated
- **CI/CD**: GitHub Actions workflow runs on every commit

## Contributing

This repository is primarily maintained through automated extraction from ACIDBATH blog posts. If you find issues:

1. Check the [original blog post](https://acidbath.sh) for context
2. Open an issue describing the problem
3. Reference the specific example and blog post

## License

Code examples are provided as-is for educational and reference purposes. See individual examples for specific licensing information.

## Related

- **Blog:** [acidbath.sh](https://acidbath.sh)
- **Main Repository:** [acidbath2](https://github.com/ameno-/acidbath2)

## POC Rule

> **POC Rule:** All code must be working, copy-paste code.

Every example in this repository adheres to the POC Rule. If you find code that doesn't work as documented, please open an issue.
