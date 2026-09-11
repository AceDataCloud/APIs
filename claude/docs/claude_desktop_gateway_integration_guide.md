# Claude Desktop third-party inference gateway

This configures Claude Desktop's **Third-Party Inference Gateway**, not Claude Code or the Claude Desktop MCP Connector.

## Configure the gateway

1. In Claude Desktop, open **Help → Troubleshooting → Enable Developer Mode**.
2. Select **Developer → Configure Third-Party Inference…** and choose **Gateway**.
3. Enter the following values, then select **Apply Changes** and **Save & Restart**:

| Field | Value |
| --- | --- |
| Gateway base URL | `https://api.acedata.cloud` |
| Gateway API key | Your Ace Data Cloud API Key |
| Gateway auth scheme | `bearer` |
| Credential kind | `Static API key` |

## Verify

After restarting, select an available model, send `Reply only OK`, and run a simple tool task. The gateway supports `/v1/models`, `/v1/messages`, tool calls, and `tool_result` continuations. Prompt-cache fields are preserved.

If authentication fails, verify the API Key. If no model appears, recheck the configuration and fully restart Claude Desktop. When requesting support, provide the trace ID rather than the API Key.

## Official references

- [Claude Desktop third-party inference installation](https://claude.com/docs/third-party/claude-desktop/installation)
- [Claude Desktop third-party inference configuration](https://claude.com/docs/third-party/claude-desktop/configuration)
