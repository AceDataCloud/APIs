# Discord Agent Proxy Integration Guide

Discord Agent Proxy is an independently deployed service that stores your Discord account credentials, maintains a persistent connection to Discord, and exposes that account's capabilities through **MCP** and **REST API** interfaces — letting AI clients or programs operate Discord on your behalf.

```
AI client  ──MCP /mcp──┐
                        ├─→ Discord Agent Proxy ──→ Discord
Your app  ──REST /api──┘      (holds your credentials)
```

> ⚠️ **Read before using:** Automating a personal Discord account (self-bot) violates Discord's Terms of Service and risks account suspension. This is an inherent premise of this service: you supply your own account credentials and accept all associated risk. **Strongly recommended: use a dedicated secondary account, not your primary account.**

## Deploy the Service

Go to [Console → Applications](https://platform.acedata.cloud/console/applications), find **Discord Agent Proxy**, and create an application. Open the configuration page, enter your Discord account credentials, and deploy.

After deployment, the configuration page shows two items:

| Item | Example | Purpose |
|---|---|---|
| MCP endpoint | `https://discord-bot-xxxxxxxxxxxx.app.acedata.cloud/mcp` | Configure in AI client |
| Access token | `V0p7kAWY...` | Authentication (see below) |

### How to Obtain Discord Account Credentials

1. Log in to Discord in a desktop browser at [discord.com/app](https://discord.com/app).
2. Press `F12` to open Developer Tools and switch to the **Network** panel.
3. Click any channel in Discord and watch the request list.
4. Open any request going to `discord.com/api`. In the **Request Headers**, find the `authorization` field.
5. Copy its value.

This credential is equivalent to your account session token — **do not share it with anyone**. If it is leaked, change your Discord password to invalidate it immediately.

## Authentication

All endpoints except `/health` require the access token in the request header:

```
Authorization: ******
```

> **Note:** This service only accepts header-based authentication; URL query parameter (`?token=xxx`) authentication is not supported. Opening an endpoint directly in a browser returns `401 unauthorized` — this is expected, not a sign of deployment failure. To verify the service is running, access `/health` (no authentication required).

## Check Service Status

```bash
curl https://discord-bot-xxxxxxxxxxxx.app.acedata.cloud/health
```

Expected response:

```json
{ "status": "ok", "gateway_ready": true }
```

The `gateway_ready` field indicates whether the connection to Discord is established:

- `true` — everything is working; you can start making calls
- `false` — the service has started but has not yet connected to Discord. A few seconds are needed after a fresh deployment; if it stays `false`, the account credentials are likely invalid or expired — re-obtain them and redeploy

When `gateway_ready` is `false`, all other endpoints return `503`.

## Use in AI Clients (MCP)

Using Claude Code as an example:

```bash
claude mcp add --transport http discord \
  https://discord-bot-xxxxxxxxxxxx.app.acedata.cloud/mcp \
  --header "Authorization: ******"
```

Other MCP-compatible clients (Cursor, Claude Desktop, etc.) typically use this configuration:

```json
{
  "mcpServers": {
    "discord": {
      "type": "http",
      "url": "https://discord-bot-xxxxxxxxxxxx.app.acedata.cloud/mcp",
      "headers": {
        "Authorization": "******"
      }
    }
  }
}
```

Once configured, you can instruct the AI to operate Discord with natural language, for example:

> Check whether there are new messages in the "project-discussion" channel; if anyone asked about the release date, reply that it will be this Friday.

### Available MCP Tools

| MCP Tool | Description |
|---|---|
| `discord_whoami` | View which account the proxy is operating as |
| `discord_list_guilds` | List all servers the account has joined |
| `discord_list_channels` | List channels in a server |
| `discord_create_text_channel` | Create a text channel |
| `discord_list_members` | List server members |
| `discord_send_message` | Send a message (optionally as a reply to another message) |
| `discord_read_messages` | Read recent messages in a channel |
| `discord_edit_message` | Edit a message you previously sent |
| `discord_delete_message` | Delete a message |
| `discord_search_messages` | Search messages in a channel |
| `discord_add_reaction` | Add an emoji reaction to a message |
| `discord_pin_message` | Pin a message |
| `discord_create_dm` | Open a direct message channel with a user; returns the channel ID |
| `discord_send_dm` | Send a direct message to a user |

## Use in Programs (REST API)

All REST endpoints are mounted under `/api`. Response bodies follow the format `{"data": ...}`; errors use `{"error": "..."}`.

### Get Current Account

```bash
curl https://discord-bot-xxxxxxxxxxxx.app.acedata.cloud/api/whoami \
  -H "Authorization: ******"
```

### Send a Message

```bash
curl -X POST https://discord-bot-xxxxxxxxxxxx.app.acedata.cloud/api/messages \
  -H "Authorization: ******" \
  -H "Content-Type: application/json" \
  -d '{"channel_id": "1234567890", "content": "Hello"}'
```

Optional `reply_to` parameter to reply to a specific message:

```json
{ "channel_id": "1234567890", "content": "Got it", "reply_to": "9876543210" }
```

### Read Messages

```bash
curl "https://discord-bot-xxxxxxxxxxxx.app.acedata.cloud/api/channels/1234567890/messages?limit=20" \
  -H "Authorization: ******"
```

### Full Endpoint Reference

| Method & Path | Parameters | Description |
|---|---|---|
| `GET /api/whoami` | — | Current account information |
| `GET /api/guilds` | — | List of servers the account has joined |
| `GET /api/guilds/{guild_id}/channels` | — | Channel list for a server |
| `POST /api/guilds/{guild_id}/channels` | `{name}` | Create a text channel |
| `GET /api/guilds/{guild_id}/members` | `?limit=` (default 100) | Server member list |
| `POST /api/messages` | `{channel_id, content, reply_to?}` | Send a message |
| `GET /api/channels/{channel_id}/messages` | `?limit=` (default 50, max 100) | Read recent messages |
| `GET /api/channels/{channel_id}/messages/search` | `?q=` (required), `&limit=` (default 25) | Search messages |
| `PATCH /api/channels/{channel_id}/messages/{message_id}` | `{content}` | Edit a message |
| `DELETE /api/channels/{channel_id}/messages/{message_id}` | — | Delete a message |
| `POST /api/channels/{channel_id}/messages/{message_id}/reactions` | `{emoji}` | Add an emoji reaction |
| `POST /api/channels/{channel_id}/messages/{message_id}/pin` | — | Pin a message |
| `POST /api/dms` | `{recipient_id}` | Open a DM channel; returns channel ID |
| `POST /api/dms/send` | `{recipient_id, content}` | Send a direct message |

### How to Get Channel IDs and User IDs

In the Discord client, go to **User Settings → Advanced** and enable **Developer Mode**. Then right-click any channel or user — a "Copy ID" option appears in the context menu.

You can also enumerate them by calling `GET /api/guilds` and `GET /api/guilds/{guild_id}/channels`.

## Troubleshooting

**Returns `401 unauthorized`**

The access token is incorrect, or you are passing it via `?token=`. Confirm the token is sent in the `Authorization` request header and matches what is shown in the console.

**Returns `503`**

The connection to Discord has not been established. Access `/health` to check `gateway_ready`. If it stays `false` for a long time, account credentials have likely expired — re-obtain them and redeploy.

**Returns `403` or `404`**

The account does not have the required permissions (for example, not in the server, or not allowed to post in that channel), or an ID is incorrect. These errors come from Discord, not the proxy service.

**Returns `429`**

Discord's rate limit has been triggered. The `retry_after` field in the response gives the recommended wait time in seconds. Reduce the call frequency.

**Account suspended after sending messages**

As noted above, automating a personal Discord account violates Discord's Terms of Service. Use a dedicated secondary account and keep operation frequency low; avoid mass-messaging and other sensitive behaviors.

## Support

For support, visit [platform.acedata.cloud/support](https://platform.acedata.cloud/support).
