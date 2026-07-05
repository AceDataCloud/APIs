# Codex API

Codex CLI is an open-source local programming agent launched by OpenAI. It can read code, modify files, run commands, and assist with development tasks within the terminal. Through the Ace Data Cloud proxy, you can use Codex CLI at a lower cost without subscribing to an official OpenAI account separately.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - OpenAI](https://platform.acedata.cloud/documents/openai)

Keywords: codex, codex-cli, openai, agentic-coding, terminal-cli, vscode-extension, responses-api, ai-api, developer-tools, Ace Data Cloud

## Why Use Codex on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready OpenAI Responses API proxy served from [https://api.acedata.cloud](https://api.acedata.cloud)
- No separate OpenAI subscription required — use your Ace Data Cloud API token
- English integration guides for Terminal CLI and VS Code

## Overview

Codex CLI is OpenAI's open-source local programming agent. It supports custom model providers through a `~/.codex/config.toml` configuration file, making it straightforward to point it at Ace Data Cloud's OpenAI Responses compatible interface (`/v1/responses`). The VS Code extension shares the same configuration layer as the CLI.

## Application Process

To use Codex via Ace Data Cloud, open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token. New accounts receive free starter credit.

## Quick Start

- Base URL: [https://api.acedata.cloud/v1](https://api.acedata.cloud/v1)
- Service page: [OpenAI on Ace Data Cloud](https://platform.acedata.cloud/documents/openai)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
# Install Codex CLI
npm install -g @openai/codex

# Set your API token
export ACEDATACLOUD_API_KEY="YOUR_API_KEY"

# Create Codex configuration
mkdir -p ~/.codex
cat > ~/.codex/config.toml << 'EOF'
model_provider = "acedatacloud"
model = "gpt-5"
model_reasoning_effort = "high"

[model_providers.acedatacloud]
name = "Ace Data Cloud"
base_url = "https://api.acedata.cloud/v1"
env_key = "ACEDATACLOUD_API_KEY"
wire_api = "responses"
EOF

# Run Codex in your project
cd /path/to/your/project
codex
```

## Guides

Explore the integration guides for Codex across different platforms.

| Platform | Description | Integration Guide |
| -------- | ----------- | ----------------- |
| **Terminal (CLI)** | Core experience — run `codex` in any terminal | [Terminal Integration Guide](docs/codex_terminal_integration_guide.md) |
| **VS Code** | Official extension for chat, file references, and diff previews in the editor sidebar | [VS Code Integration Guide](docs/codex_vscode_integration_guide.md) |
