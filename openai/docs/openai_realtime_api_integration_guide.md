# OpenAI Realtime API Integration and Usage

The OpenAI Realtime API provides low-latency speech-to-speech over a WebSocket using the OpenAI Realtime GA event protocol.

## Endpoint

```text
wss://api.acedata.cloud/v1/realtime?model=gpt-realtime
```

The OpenAPI entry is `GET /v1/realtime` and upgrades to WebSocket (`101 Switching Protocols`) on success.

## Authentication

Server-to-server clients should send an `Authorization: ******` header. Browser clients can pass the token with the WebSocket subprotocol format `realtime, acedata-token.<token>`.

## Usage Notes

- Transport audio is fixed to PCM16 at 24 kHz mono.
- Client and server exchange Realtime JSON events such as `session.update`, `input_audio_buffer.append`, `response.create`, `response.output_audio.delta`, and `response.done`.
- The relay fixes connection model, output voice, transcription, and noise-reduction settings; choose the model and voice when connecting.
- `session.update` may change GA fields including `instructions`, `tools`, `tool_choice`, `output_modalities`, `include`, `prompt`, `reasoning`, `parallel_tool_calls`, `tracing`, and `truncation`.
- `audio.input.turn_detection` can be set to `null`, `server_vad`, or `semantic_vad` with their documented controls.
- Attempts to change fixed fields, exceed the output-token cap, use legacy beta fields, or send unknown fields return a recoverable `error` event. The WebSocket remains open.
- Billing is calculated per assistant turn from `response.done.usage`, with audio and text tokens priced separately.

## JavaScript Connection Example

```js
const token = "******";
const ws = new WebSocket(
  "wss://api.acedata.cloud/v1/realtime?model=gpt-realtime",
  ["realtime", `acedata-token.${token}`]
);

ws.addEventListener("open", () => {
  ws.send(JSON.stringify({
    type: "session.update",
    session: {
      instructions: "You are a helpful assistant.",
      output_modalities: ["audio", "text"]
    }
  }));
});

ws.addEventListener("message", (event) => {
  const message = JSON.parse(event.data);
  console.log(message.type, message);
});
```
