# OpenAI Realtime API Application and Usage

The OpenAI Realtime API provides low-latency speech-to-speech interaction over WebSocket using the OpenAI Realtime GA event protocol.

## Application Process

Open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token. A single API Token works across every service on the platform.

## Endpoint

```http
GET https://api.acedata.cloud/v1/realtime
```

Connect over WebSocket:

```text
wss://api.acedata.cloud/v1/realtime?model=gpt-realtime-2.1
```

## Query Parameters

| Field | Type | Required | Description |
| ---- | ---- | ---- | ---- |
| `model` | string | Yes | Realtime model to use. Supported values are `gpt-realtime-2.1`, `gpt-realtime-2.1-mini`, `gpt-realtime-2`, `gpt-realtime`, and `gpt-realtime-mini`. Defaults to `gpt-realtime-2.1`. |
| `voice` | string | No | Output voice selected when the connection is established. Supported values are `alloy`, `ash`, `ballad`, `coral`, `echo`, `sage`, `shimmer`, `verse`, `marin`, and `cedar`. Defaults to `alloy`. |

## Authentication

Use the Ace Data Cloud API token when opening the WebSocket connection. Server-side clients can send an `Authorization: ******` header. Browser clients should pass the token through `Sec-WebSocket-Protocol` as:

```text
realtime, acedata-token.<token>
```

## Protocol Notes

Client and server exchange Realtime JSON events such as:

- `session.update`
- `input_audio_buffer.append`
- `response.create`
- `response.output_audio.delta`
- `response.done`

The relay fixes the connection model, PCM16 24 kHz mono transport, output voice, transcription, and noise-reduction settings when the connection is established. A `session.update` may change GA fields such as `instructions`, `tools`, `tool_choice`, `output_modalities`, `include`, `prompt`, `reasoning`, `parallel_tool_calls`, `tracing`, `truncation`, and `audio.input.turn_detection`.

Attempts to change fixed fields, exceed the output-token cap, use legacy beta fields, or send unknown fields return a recoverable `error` event. The WebSocket remains open. Billing is per assistant turn from `response.done.usage`, with audio and text tokens priced separately.

## Responses

- `101 Switching Protocols`: WebSocket established.
- `401 Unauthorized`: Missing or invalid bearer token.
- `403 Forbidden`: Insufficient balance.
