The OpenAI Realtime API establishes an authenticated WebSocket session for realtime model interaction.

## Authentication

Send your Ace Data Cloud API Token with HTTP bearer authentication during the WebSocket upgrade.

## Query Parameters

| Field | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `model` | string | Yes | `gpt-realtime-2.1` | `gpt-realtime-2.1`, `gpt-realtime-2.1-mini`, `gpt-realtime-2`, `gpt-realtime`, or `gpt-realtime-mini`. |
| `voice` | string | No | `alloy` | `alloy`, `ash`, `ballad`, `coral`, `echo`, `sage`, `shimmer`, `verse`, `marin`, or `cedar`. |

## Connect

Connect to:

```text
wss://api.acedata.cloud/v1/realtime?model=gpt-realtime-2.1&voice=alloy
```

Include the authorization header in the WebSocket handshake:

```http
Authorization: ******
```

A successful request returns HTTP `101 Switching Protocols`. The endpoint returns `401` for invalid authentication and `403` when access is denied.
