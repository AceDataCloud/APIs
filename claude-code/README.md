# Claude Code API

Claude Code is an agentic coding tool launched by Anthropic, usable in terminals, IDEs (VS Code, JetBrains), and CI/CD pipelines (GitHub Actions). Ace Data Cloud provides a proxy service so you can access Claude Code at a lower cost without a direct Anthropic subscription.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Claude Code](https://platform.acedata.cloud/documents/claude-messages)

Keywords: claude-code, anthropic, agentic-coding, terminal-cli, vscode-extension, jetbrains-plugin, github-actions, ai-api, developer-tools, Ace Data Cloud

## Why Use Claude Code on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready proxy endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- No official Anthropic subscription required — use your Ace Data Cloud API token
- English integration guides for Terminal, VS Code, JetBrains, and GitHub Actions

## Overview

Claude Code is Anthropic's **Agentic Coding** tool — one of the most powerful programming agents available. It understands your codebase, can read and edit files, run commands, create commits, open PRs, and more. Ace Data Cloud proxies Claude Code's API, letting you configure any Claude Code client to send requests to `https://api.acedata.cloud` using your Ace Data Cloud API token.

## Application Process

To use Claude Code via Ace Data Cloud, open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token. New accounts receive free starter credit.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Claude Code on Ace Data Cloud](https://platform.acedata.cloud/documents/claude-messages)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
# Set environment variables, then run claude in your project directory
export ANTHROPIC_AUTH_TOKEN="YOUR_API_KEY"
export ANTHROPIC_BASE_URL="https://api.acedata.cloud"
cd /path/to/your/project
claude
```

## Guides

Explore the integration guides for Claude Code across different platforms.

| Platform | Description | Integration Guide |
| -------- | ----------- | ----------------- |
| **Terminal (CLI)** | Core experience — run `claude` in any terminal | [Terminal Integration Guide](docs/claude_code_terminal_integration_guide.md) |
| **VS Code** | Native extension with inline Diff, `@`-mentions, and plan reviews | [VS Code Integration Guide](docs/claude_code_vscode_integration_guide.md) |
| **JetBrains IDEs** | Plugin for IntelliJ IDEA, PyCharm, WebStorm, GoLand, and more | [JetBrains Integration Guide](docs/claude_code_jetbrains_integration_guide.md) |
| **GitHub Actions** | Automate code reviews and Issue handling with `@claude` | [GitHub Actions Integration Guide](docs/claude_code_github_actions_integration_guide.md) |
