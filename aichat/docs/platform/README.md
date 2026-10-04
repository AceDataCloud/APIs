<!-- Generated from PlatformBackend; edit the backend source. -->
# API reference

These are the public HTTP API contracts. Native MCP tools and CLI commands are described in the package README.

## AI Dialogue

| Method | Endpoint | Request fields |
| --- | --- | --- |
| POST | `/aichat2/conversations` | `action`, `id`, `model`, `question`, `message`, `stateful`, `references`, `preset`, `max_turns`, `async`, `callback_url`, `allowed_skills`, `allowed_mcp_servers`, `unattended_policy`, `tool_results`, `messages`, `title`, `user_id`, `application_id`, `model_group`, `offset`, `limit` |
| POST | `/aichat/conversations` | `id`, `model`, `preset`, `question`, `stateful`, `references` |

Full schema: [aichat.json](openapi/aichat.json).

### Guides

- [development_aichat2_conversations.md](guides/development_aichat2_conversations.md)
- [development_aichat_conversations.md](guides/development_aichat_conversations.md)

Source: [PlatformBackend@bdae773e02f3](https://github.com/AceDataCloud/PlatformBackend/tree/bdae773e02f3f51d2896eef497b569748577b753).
