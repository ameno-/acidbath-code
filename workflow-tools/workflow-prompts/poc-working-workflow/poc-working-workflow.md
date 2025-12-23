---
description: Analyze a file and create implementation plan
allowed-tools: Read, Glob, Grep, Write
argument-hint: <file_path>
---

# File Analysis and Planning Agent

## Purpose
Analyze the provided file and create a detailed implementation plan for improvements.

## Variables
- **target_file**: $ARGUMENTS (the file to analyze)
- **output_dir**: ./specs

## Workflow

1. **Read the target file**
   - Load the complete contents of {{target_file}}
   - Note the file type, structure, and purpose

2. **Analyze the codebase context**
   - Use Glob to find related files (same directory, similar names)
   - Use Grep to find references to functions/classes in this file
   - Identify dependencies and dependents

3. **Identify improvement opportunities**
   - List potential refactoring targets
   - Note any code smells or anti-patterns
   - Consider performance optimizations
   - Check for missing error handling

4. **Create implementation plan**
   - For each improvement, specify:
     - What to change
     - Why it matters
     - Files affected
     - Risk level (low/medium/high)

5. **Write the plan to file**
   - Save to {{output_dir}}/{{filename}}-plan.md
   - Include timestamp and file hash for tracking

## Output Format
file_analyzed: {{target_file}}
timestamp: {{current_time}}
improvements:
  - id: 1
    type: refactor|performance|error-handling|cleanup
    description: "What to change"
    rationale: "Why it matters"
    files_affected: [list]
    risk: low|medium|high
    effort: small|medium|large

## Early Returns
- If {{target_file}} doesn't exist, stop and report error
- If file is binary or unreadable, stop and explain
- If no improvements found, report "file looks good" with reasoning
