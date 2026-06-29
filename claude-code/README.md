# Claude Code

Claude Code is a programming AI agent launched by Anthropic, which can be used in various environments such as terminals, IDEs, and CI/CD pipelines. By using the AceData Cloud proxy, you can access Claude Code at a lower cost.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

Service page: [Ace Data Cloud - Claude Messages](https://platform.acedata.cloud/documents/claude-messages)

Keywords: claude-code, anthropic, agentic-coding, vscode, jetbrains, terminal, github-actions, ai-agent, developer-tools, AI API, Ace Data Cloud

## Why Use Claude Code on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

Claude Code is Anthropic's agentic coding tool, recognized as one of the world's strongest programming agents. It supports a wide range of environments including VS Code, JetBrains IDEs, the terminal CLI, and GitHub Actions. AceData Cloud provides a proxy service so you can use Claude Code without a direct Anthropic subscription.

## Application Process

To use the Claude Code proxy, first open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

A single API Token works across every service on the platform — no need to subscribe per service. New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Claude Messages on Ace Data Cloud](https://platform.acedata.cloud/documents/claude-messages)
- Docs: [Developer documentation](https://docs.acedata.cloud)

Set the following environment variables in your shell or Claude Code settings to route requests through AceData Cloud:

```bash
export ANTHROPIC_AUTH_TOKEN="{your_api_token}"
export ANTHROPIC_BASE_URL="https://api.acedata.cloud"
```

## Integration Guides

Choose the complete configuration guide for the corresponding platform based on your usage scenario:

| Platform | Description | Tutorial Link |
|----------|-------------|--------------|
| **VS Code** | Native extension, supports inline Diff, @-mentions, and scheduled reviews | [VS Code Configuration Guide](docs/claude_code_vscode.md) |
| **Terminal (CLI)** | Core experience, start by running `claude` in any terminal | [Terminal Configuration Guide](docs/claude_code_terminal.md) |
| **JetBrains IDE** | Supports IntelliJ IDEA, PyCharm, WebStorm, and other IDEs in the family | [JetBrains Configuration Guide](docs/claude_code_jetbrains.md) |
| **GitHub Actions** | Automate code reviews and Issue handling with `@claude` | [GitHub Actions Configuration Guide](docs/claude_code_github_actions.md) |
