# Claude Code Configuration

Use Claude Code with Ace Data Cloud in terminals, supported IDEs, and CI/CD workflows.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![Tool](https://img.shields.io/badge/type-AI%20coding%20agent-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

Service page: [Claude Messages on Ace Data Cloud](https://platform.acedata.cloud/documents/claude-messages)

## Overview

Configure Claude Code to use the Ace Data Cloud proxy with an API token from the [console](https://platform.acedata.cloud/console/applications):

```bash
export ANTHROPIC_BASE_URL="https://api.acedata.cloud"
export ANTHROPIC_AUTH_TOKEN="{token}"
export CLAUDE_CODE_AUTO_COMPACT_WINDOW="850000"
```

`CLAUDE_CODE_AUTO_COMPACT_WINDOW` sets the automatic-compaction trigger to approximately 850,000 tokens, reserving room for tool results and final responses without changing the model context limit.

## Configuration Guides

| Platform | Description | Guide |
| --- | --- | --- |
| Terminal (CLI) | Run `claude` in any terminal | [Terminal Configuration Guide](https://platform.acedata.cloud/documents/claude-code-terminal-integration) |
| VS Code | Native extension with inline diffs and `@` mentions | [VS Code Configuration Guide](https://platform.acedata.cloud/documents/claude-code-vscode-integrations) |
| JetBrains IDEs | IntelliJ IDEA, PyCharm, WebStorm, GoLand, and more | [JetBrains Configuration Guide](docs/claude_code_jetbrains_integration_guide.md) |
| CC Switch | Desktop GUI for switching service configurations | [CC Switch Configuration Guide](https://platform.acedata.cloud/documents/claude-code-cc-switch-integration) |
| GitHub Actions | Automate Issue and pull-request tasks with `@claude` | [GitHub Actions Configuration Guide](https://platform.acedata.cloud/documents/claude-code-github-actions-integration) |
