# OpenAI Realtime API Application and Usage

The OpenAI Realtime API provides low-latency speech-to-speech communication over a WebSocket using the OpenAI Realtime GA event protocol.

## Application Process

Use an Ace Data Cloud API token from the [console](https://platform.acedata.cloud/console/applications). Authenticate the WebSocket connection with an `Authorization` bearer token. Browser clients can pass `realtime, acedata-token.<token>` through `Sec-WebSocket-Protocol`.

## Endpoint

```text
GET wss://api.acedata.cloud/v1/realtime?model=gpt-realtime-2.1
```

## Query Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| `model` | Yes | Realtime model. Use `gpt-realtime-2.1` for best quality or `gpt-realtime-2.1-mini` for lower cost. Older compatible IDs are `gpt-realtime-2`, `gpt-realtime`, and `gpt-realtime-mini`. |
| `voice` | No | Output voice selected at connection time. Supported values are `alloy`, `ash`, `ballad`, `coral`, `echo`, `sage`, `shimmer`, `verse`, `marin`, and `cedar`; defaults to `alloy`. |

## Basic Usage

```javascript
const token = "******";
const ws = new WebSocket(
  "wss://api.acedata.cloud/v1/realtime?model=gpt-realtime-2.1&voice=alloy",
  ["realtime", `acedata-token.${token}`]
);

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: "session.update",
    session: {
      instructions: "You are a helpful voice assistant."
    }
  }));
};

ws.onmessage = (event) => {
  console.log(event.data);
};
```

## Event Protocol

Client and server exchange Realtime JSON events such as `session.update`, `input_audio_buffer.append`, `response.create`, `response.output_audio.delta`, and `response.done`. Supported session updates include `instructions`, `tools`, `tool_choice`, `output_modalities`, `include`, `prompt`, `reasoning`, `parallel_tool_calls`, `tracing`, and `truncation`.

Attempts to change fixed connection fields, exceed the output-token cap, use legacy beta fields, or send unknown fields return a recoverable `error` event while keeping the WebSocket open.

## Responses

A successful upgrade returns `101 Switching Protocols`. Missing or invalid credentials return `401`; insufficient balance returns `403`.

## Conclusion

Use this endpoint for realtime voice interactions that need low-latency bidirectional audio and text events.
