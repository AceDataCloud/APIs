# Discord Agent Proxy

Deploy a personal Discord automation proxy — operate Discord accounts through **MCP** and **REST API** interfaces, enabling AI clients and programs to automate Discord on your behalf.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-Agent%20Proxy-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

Service page: [Ace Data Cloud - Discord Agent Proxy](https://platform.acedata.cloud/console/applications)

Keywords: discord-bot, discord-agent, discord-proxy, discord-api, discord-mcp, discord-automation, rest-api, mcp-server, Ace Data Cloud

## Overview

Discord Agent Proxy is an **independently deployed** service. It stores your own Discord account credentials, maintains a persistent connection to Discord, and exposes that account's capabilities through both an **MCP** interface and a **REST API** — letting AI clients or programs operate Discord on your behalf.

The container includes **no AI models** — it only executes commands issued by your AI client (Claude, Cursor, etc.) or your own program.

```
AI client  ──MCP /mcp──┐
                        ├─→ Discord Agent Proxy ──→ Discord
Your app  ──REST /api──┘      (holds your credentials)
```

> ⚠️ **Important:** Automating a personal Discord account (self-bot) violates Discord's Terms of Service and risks account suspension. This service requires you to supply your own account credentials; you accept all associated risk. **Strongly recommended: use a dedicated secondary account, not your primary account.**

## Deploy the Service

1. Go to [Console → Applications](https://platform.acedata.cloud/console/applications), find **Discord Agent Proxy**, and create an application.
2. Open the configuration page, enter your Discord account credentials, and deploy.

After deployment, the configuration page shows:

| Item | Example | Purpose |
|---|---|---|
| MCP endpoint | `https://discord-bot-xxxxxxxxxxxx.app.acedata.cloud/mcp` | Configure in AI client |
| Access token | `V0p7kAWY...` | Authentication |

## Quick Start

Check service health (no authentication required):

```bash
curl https://discord-bot-xxxxxxxxxxxx.app.acedata.cloud/health
```

Expected response:

```json
{ "status": "ok", "gateway_ready": true }
```

Send a message via REST:

```bash
curl -X POST https://discord-bot-xxxxxxxxxxxx.app.acedata.cloud/api/messages \
  -H "Authorization: ******" \
  -H "Content-Type: application/json" \
  -d '{"channel_id": "1234567890", "content": "Hello"}'
```

## APIs and Guides

| Guide | Description |
|---|---|
| [Discord Agent Proxy Integration Guide](docs/discord_agent_proxy_guide.md) | Full setup, MCP configuration, REST API reference, and troubleshooting |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [API Documentation](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

For support, visit [platform.acedata.cloud/support](https://platform.acedata.cloud/support).
